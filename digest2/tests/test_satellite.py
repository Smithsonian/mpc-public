"""Tests for satellite / roving observer position handling.

Regression tests for the bug where the Python wrapper ignored the ADES
sys/pos1/pos2/pos3 fields (and the MPC 80-column 's'/'v' second lines),
silently scoring all space-based observations from the geocenter while
the C CLI used the supplied observer positions.
"""

import subprocess
from pathlib import Path

import pytest

from digest2 import Digest2
from digest2.observation import (
    _KM_TO_AU,
    _roving_position,
    Observation,
    parse_ades_psv,
    parse_ades_xml,
    parse_mpc80,
    parse_mpc80_file,
)


# ---------------------------------------------------------------------------
# Test data builders
# ---------------------------------------------------------------------------

# Synthetic NEO Surveyor (C58) tracklet, observer ~0.01 AU from the geocenter
# so that ignoring the observer position visibly changes the scores.
SAT_OBS = [
    ("2025-03-01T01:00:00.000Z", 100.000000, 10.000000, 20.5,
     (1350000.0, -550000.0, -230000.0)),
    ("2025-03-01T02:00:00.000Z", 100.010000, 10.003000, 20.6,
     (1351000.0, -548000.0, -229000.0)),
    ("2025-03-01T03:00:00.000Z", 100.020000, 10.006000, 20.4,
     (1352000.0, -546000.0, -228000.0)),
]


def _write_sat_xml(path, with_pos=True, sys="ICRF_KM", stn="C58"):
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<ades version="2017">']
    for (t, ra, dec, mag, pos) in SAT_OBS:
        parts.append("  <optical>")
        parts.append("    <trkSub>ST001aa</trkSub>")
        parts.append("    <mode>CCD</mode>")
        parts.append(f"    <stn>{stn}</stn>")
        if with_pos:
            parts.append(f"    <sys>{sys}</sys>")
            parts.append("    <ctr>399</ctr>")
            parts.append(f"    <pos1>{pos[0]}</pos1>")
            parts.append(f"    <pos2>{pos[1]}</pos2>")
            parts.append(f"    <pos3>{pos[2]}</pos3>")
        parts.append(f"    <obsTime>{t}</obsTime>")
        parts.append(f"    <ra>{ra:.6f}</ra>")
        parts.append(f"    <dec>{dec:.6f}</dec>")
        parts.append("    <rmsRA>0.15</rmsRA>")
        parts.append("    <rmsDec>0.15</rmsDec>")
        parts.append(f"    <mag>{mag}</mag>")
        parts.append("    <band>V</band>")
        parts.append("  </optical>")
    parts.append("</ades>")
    Path(path).write_text("\n".join(parts) + "\n")
    return str(path)


def _write_sat_psv(path):
    header = ("trkSub |mode|stn |sys    |ctr|pos1      |pos2      |pos3      "
              "|obsTime                 |ra         |dec        |rmsRA|rmsDec|mag  |band")
    lines = [header]
    for (t, ra, dec, mag, pos) in SAT_OBS:
        lines.append(
            f"ST001aa|CCD |C58 |ICRF_KM|399|{pos[0]}|{pos[1]}|{pos[2]}"
            f"|{t}|{ra:.6f}|{dec:.6f}|0.15 |0.15  |{mag}|V"
        )
    Path(path).write_text("\n".join(lines) + "\n")
    return str(path)


# MPC 80-column ground-based tracklet (from sample.obs) rewritten as
# satellite observations: note2 'S', station C57, each followed by an 's'
# second line carrying a TESS-like geocentric position in km.
MPC80_GROUND_LINES = [
    "     K16S99K 1C2022 12 25.38496508 32 36.283+17 10 35.94         21.98GV     G96",
    "     K16S99K 1C2022 12 25.39527308 32 35.635+17 10 37.27         21.72GV     G96",
    "     K16S99K 1C2022 12 25.40040208 32 35.473+17 10 37.38         21.31GV     G96",
]

MPC80_SAT_POSITIONS = [
    (235000.123, -180000.456, 95000.789),
    (235100.321, -179900.654, 95100.987),
    (235200.213, -179800.564, 95200.879),
]


def _sat_second_line(parent_line, x, y, z, code="C57", note2="s", flag="1"):
    """Build an MPC 80-column satellite/roving second line."""
    chars = [" "] * 80
    chars[0:12] = parent_line[0:12]
    chars[14] = note2
    chars[15:32] = parent_line[15:32]
    chars[32] = flag
    chars[34:45] = f"{x:+.3f}".ljust(11)
    chars[46:57] = f"{y:+.3f}".ljust(11)
    chars[58:69] = f"{z:+.3f}".ljust(11)
    chars[77:80] = code
    return "".join(chars)


def _write_sat_obs80(path, with_pos=True, code="C57"):
    lines = []
    for ground, (x, y, z) in zip(MPC80_GROUND_LINES, MPC80_SAT_POSITIONS):
        sat_line = ground[:14] + "S" + ground[15:77] + code
        lines.append(sat_line)
        if with_pos:
            lines.append(_sat_second_line(sat_line, x, y, z, code=code))
    Path(path).write_text("\n".join(lines) + "\n")
    return str(path)


def _cli(args, timeout=120):
    """Run the C CLI from the data directory; skip if not built."""
    project_dir = Path(__file__).resolve().parents[1]
    data_dir = project_dir / "digest2"
    binary = data_dir / "digest2"
    if not binary.exists():
        pytest.skip(f"digest2 binary not found at {binary} "
                    "(run: cd digest2/digest2 && make)")
    return subprocess.run(
        [str(binary)] + list(args),
        cwd=data_dir,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


@pytest.fixture
def cli_config_path(tmp_path):
    """Config accepted by both the C CLI and the Python wrapper.

    Listing classes restricts the CLI's computed-class set, which the
    Python side must mirror (classes=["NEO", "MB1"]) for identical scores.
    """
    p = tmp_path / "test.config"
    p.write_text("repeatable\nrms\nraw\nnoid\nNEO\nMB1\n")
    return str(p)


def _parse_cli_scores(stdout):
    """Parse 'Desig. RMS NEOraw NEOnid MB1raw MB1nid' CLI output lines."""
    results = {}
    for line in stdout.strip().splitlines():
        if not line or "Desig" in line or line.startswith("-"):
            continue
        parts = line.split()
        if len(parts) >= 6:
            results[parts[0]] = [float(v) for v in parts[1:6]]
    return results


# ---------------------------------------------------------------------------
# Parser unit tests (no model required)
# ---------------------------------------------------------------------------
class TestAdesXmlObserverPosition:

    def test_icrf_km_position_parsed(self, tmp_path):
        path = _write_sat_xml(tmp_path / "sat.xml", sys="ICRF_KM")
        tracklets = parse_ades_xml(path)
        obs_list = tracklets["ST001aa"]
        assert len(obs_list) == 3
        for obs, (_, _, _, _, pos) in zip(obs_list, SAT_OBS):
            assert obs.spacebased is True
            assert obs.earth_obs == [pos[0] * _KM_TO_AU,
                                     pos[1] * _KM_TO_AU,
                                     pos[2] * _KM_TO_AU]

    def test_icrf_au_position_not_scaled(self, tmp_path):
        path = _write_sat_xml(tmp_path / "sat_au.xml", sys="ICRF_AU")
        obs = parse_ades_xml(path)["ST001aa"][0]
        assert obs.spacebased is True
        assert obs.earth_obs == list(SAT_OBS[0][4])

    def test_wgs84_roving_position(self, tmp_path):
        path = _write_sat_xml(tmp_path / "rov.xml", sys="WGS84", stn="247")
        obs = parse_ades_xml(path)["ST001aa"][0]
        assert obs.spacebased is True
        x, y, z = SAT_OBS[0][4]
        expected = [v * _KM_TO_AU for v in _roving_position(x, y, z)]
        assert obs.earth_obs == expected

    def test_no_pos_is_ground_based(self, tmp_path):
        path = _write_sat_xml(tmp_path / "nopos.xml", with_pos=False)
        obs = parse_ades_xml(path)["ST001aa"][0]
        assert obs.spacebased is False
        assert obs.earth_obs == [0.0, 0.0, 0.0]


class TestAdesPsvObserverPosition:

    def test_icrf_km_position_parsed(self, tmp_path):
        path = _write_sat_psv(tmp_path / "sat.psv")
        obs_list = parse_ades_psv(path)["ST001aa"]
        assert len(obs_list) == 3
        for obs, (_, _, _, _, pos) in zip(obs_list, SAT_OBS):
            assert obs.spacebased is True
            assert obs.earth_obs == [pos[0] * _KM_TO_AU,
                                     pos[1] * _KM_TO_AU,
                                     pos[2] * _KM_TO_AU]

    def test_none_pos_is_ground_based(self, tmp_path):
        header = ("trkSub |stn |sys |pos1|pos2|pos3"
                  "|obsTime                 |ra        |dec       |mag  |band")
        row = ("ST001aa|G96 |None|None|None|None"
               "|2025-03-01T01:00:00.000Z|100.000000|10.000000 |20.5 |V")
        p = tmp_path / "ground.psv"
        p.write_text(header + "\n" + row + "\n")
        obs = parse_ades_psv(str(p))["ST001aa"][0]
        assert obs.spacebased is False
        assert obs.earth_obs == [0.0, 0.0, 0.0]


class TestMpc80SecondLine:

    def test_satellite_km_flag_scaled(self, tmp_path):
        path = _write_sat_obs80(tmp_path / "sat.obs")
        obs_list = parse_mpc80_file(path)["     K16S99K"]
        assert len(obs_list) == 3
        for obs, (x, y, z) in zip(obs_list, MPC80_SAT_POSITIONS):
            assert obs.spacebased is True
            assert obs.earth_obs == [x * _KM_TO_AU,
                                     y * _KM_TO_AU,
                                     z * _KM_TO_AU]

    def test_satellite_au_flag_not_scaled(self, tmp_path):
        ground = MPC80_GROUND_LINES[0]
        sat_line = ground[:14] + "S" + ground[15:77] + "C57"
        second = _sat_second_line(sat_line, 0.01, -0.005, 0.002, flag="2")
        p = tmp_path / "sat_au.obs"
        p.write_text(sat_line + "\n" + second + "\n")
        obs = parse_mpc80_file(str(p))["     K16S99K"][0]
        assert obs.spacebased is True
        assert obs.earth_obs == [0.01, -0.005, 0.002]

    def test_obscode_mismatch_rejected(self, tmp_path):
        ground = MPC80_GROUND_LINES[0]
        sat_line = ground[:14] + "S" + ground[15:77] + "C57"
        # Second line claims a different observatory: must be ignored.
        second = _sat_second_line(sat_line, 235000.0, -180000.0, 95000.0,
                                  code="C51")
        p = tmp_path / "mismatch.obs"
        p.write_text(sat_line + "\n" + second + "\n")
        obs = parse_mpc80_file(str(p))["     K16S99K"][0]
        assert obs.spacebased is False
        assert obs.earth_obs == [0.0, 0.0, 0.0]

    def test_sign_separated_from_digits(self, tmp_path):
        """C mustStrtod accepts '- 3471.6659'; the Python parser must too."""
        ground = MPC80_GROUND_LINES[0]
        sat_line = ground[:14] + "S" + ground[15:77] + "C57"
        chars = list(_sat_second_line(sat_line, 0.0, 0.0, 0.0))
        chars[34:45] = "- 3471.6659"
        chars[46:57] = "+ 5520.9248"
        chars[58:69] = "- 1718.8956"
        p = tmp_path / "spaced.obs"
        p.write_text(sat_line + "\n" + "".join(chars) + "\n")
        obs = parse_mpc80_file(str(p))["     K16S99K"][0]
        assert obs.spacebased is True
        assert obs.earth_obs == [-3471.6659 * _KM_TO_AU,
                                 5520.9248 * _KM_TO_AU,
                                 -1718.8956 * _KM_TO_AU]

    def test_roving_second_line(self, tmp_path):
        ground = MPC80_GROUND_LINES[0]
        # Roving 'v' lines attach to the preceding observation without an
        # obscode check (mirroring d2mpc.c parseMpcRoving).
        first = ground  # ordinary CCD observation
        second = _sat_second_line(ground, 0.5, 0.7, 2000.0, note2="v",
                                  code="247")
        p = tmp_path / "rov.obs"
        p.write_text(first + "\n" + second + "\n")
        obs = parse_mpc80_file(str(p))["     K16S99K"][0]
        assert obs.spacebased is True
        expected = [v * _KM_TO_AU for v in _roving_position(0.5, 0.7, 2000.0)]
        assert obs.earth_obs == expected


class TestMpc80DbRecords:
    """160-column database records: the MPC ``obs`` table stores satellite /
    roving observations as first line + second line concatenated in one
    ``obs80`` value. parse_mpc80 must apply the second segment's observer
    position (the digest2-service /digest2_trkid path feeds these records
    one at a time, so parse_mpc80_file's pairing never runs)."""

    @staticmethod
    def _db_record(index=0, code="C57", flag="1"):
        ground = MPC80_GROUND_LINES[index]
        x, y, z = MPC80_SAT_POSITIONS[index]
        sat_line = ground[:14] + "S" + ground[15:77] + code
        second = _sat_second_line(sat_line, x, y, z, code=code, flag=flag)
        return sat_line + second, (x, y, z)

    def test_db_record_satellite_km(self):
        record, (x, y, z) = self._db_record()
        assert len(record) == 160
        obs = parse_mpc80(record)
        assert obs is not None
        assert obs.spacebased is True
        assert obs.earth_obs == [x * _KM_TO_AU, y * _KM_TO_AU, z * _KM_TO_AU]

    def test_db_record_au_flag_not_scaled(self):
        ground = MPC80_GROUND_LINES[0]
        sat_line = ground[:14] + "S" + ground[15:77] + "C57"
        second = _sat_second_line(sat_line, 0.01, -0.005, 0.002, flag="2")
        obs = parse_mpc80(sat_line + second)
        assert obs is not None
        assert obs.spacebased is True
        assert obs.earth_obs == [0.01, -0.005, 0.002]

    def test_db_record_roving(self):
        ground = MPC80_GROUND_LINES[0]
        second = _sat_second_line(ground, 0.5, 0.7, 2000.0, note2="v",
                                  code="247")
        obs = parse_mpc80(ground + second)
        assert obs is not None
        assert obs.spacebased is True
        expected = [v * _KM_TO_AU for v in _roving_position(0.5, 0.7, 2000.0)]
        assert obs.earth_obs == expected

    def test_plain_80_column_lines_unchanged(self):
        # Ordinary ground-based line.
        obs = parse_mpc80(MPC80_GROUND_LINES[0])
        assert obs is not None
        assert obs.spacebased is False
        # A bare satellite first line (no second segment) keeps the previous
        # behaviour: parsed, geocentric.
        ground = MPC80_GROUND_LINES[0]
        sat_line = ground[:14] + "S" + ground[15:77] + "C57"
        obs = parse_mpc80(sat_line)
        assert obs is not None
        assert obs.spacebased is False

    def test_padded_line_not_treated_as_record(self):
        # Whitespace padding beyond column 80 must not change parsing
        # (regression guard: only an 's'/'v' note2 at column 95 marks a
        # two-line record).
        for padded_len in (95, 120, 160):
            obs = parse_mpc80(MPC80_GROUND_LINES[0].ljust(padded_len))
            assert obs is not None
            assert obs.spacebased is False
            assert obs.earth_obs == [0.0, 0.0, 0.0]

    def test_malformed_second_segment_rejects_record(self):
        # Obscode mismatch between the two segments: reject the record
        # rather than silently scoring geocentrically.
        ground = MPC80_GROUND_LINES[0]
        sat_line = ground[:14] + "S" + ground[15:77] + "C57"
        second = _sat_second_line(sat_line, 235000.0, -180000.0, 95000.0,
                                  code="C51")
        assert parse_mpc80(sat_line + second) is None
        # Garbage position fields: likewise rejected.
        chars = list(_sat_second_line(sat_line, 0.0, 0.0, 0.0))
        chars[34:45] = "not-a-float"
        assert parse_mpc80(sat_line + "".join(chars)) is None

    def test_db_record_scores_match_file_parse(self, tmp_path, model_path,
                                               obscodes_path,
                                               empty_config_path):
        """classify_tracklet on 160-column DB records must score identically
        to classify_file on the equivalent two-line file."""
        records = []
        for i in range(len(MPC80_GROUND_LINES)):
            record, _ = self._db_record(index=i)
            records.append(record)
        file_path = _write_sat_obs80(tmp_path / "sat.obs")

        with Digest2(model_path=model_path, obscodes_path=obscodes_path,
                     config_path=empty_config_path, repeatable=True) as d2:
            obs_list = [parse_mpc80(r) for r in records]
            assert all(o is not None and o.spacebased for o in obs_list)
            r_records = d2.classify_tracklet(obs_list)
            r_file = d2.classify_file(file_path)[0]

        assert r_records.raw.NEO == r_file.raw.NEO
        assert r_records.noid.NEO == r_file.noid.NEO


class TestObservationToTuple:

    def test_earth_obs_in_tuple(self):
        obs = Observation(mjd=60000.0, ra=100.0, dec=10.0, obscode="C58",
                          spacebased=True, earth_obs=[0.009, -0.0037, -0.0015])
        t = obs.to_tuple(site_index=1234)
        assert len(t) == 11
        assert t[7] == 1
        assert t[8:11] == (0.009, -0.0037, -0.0015)

    def test_ground_based_defaults(self):
        obs = Observation(mjd=60000.0, ra=100.0, dec=10.0, obscode="G96")
        t = obs.to_tuple(site_index=1696)
        assert len(t) == 11
        assert t[7] == 0
        assert t[8:11] == (0.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# Scoring tests (require model + obscodes)
# ---------------------------------------------------------------------------
class TestSatelliteScoring:

    def test_position_changes_scores(self, tmp_path, model_path,
                                     obscodes_path, empty_config_path):
        """Observer position must influence the scores (the original bug
        produced identical scores with and without pos1/pos2/pos3)."""
        with_pos = _write_sat_xml(tmp_path / "sat.xml")
        without_pos = _write_sat_xml(tmp_path / "nopos.xml", with_pos=False)

        with Digest2(model_path=model_path, obscodes_path=obscodes_path,
                     config_path=empty_config_path, repeatable=True) as d2:
            r_with = d2.classify_file(with_pos)[0]
            r_without = d2.classify_file(without_pos)[0]

        assert abs(r_with.raw.NEO - r_without.raw.NEO) > 2.0
        assert abs(r_with.raw.MB1 - r_without.raw.MB1) > 2.0

    def test_mpc80_satellite_position_changes_scores(
            self, tmp_path, model_path, obscodes_path, empty_config_path):
        with_pos = _write_sat_obs80(tmp_path / "sat.obs")
        without_pos = _write_sat_obs80(tmp_path / "nopos.obs", with_pos=False)

        with Digest2(model_path=model_path, obscodes_path=obscodes_path,
                     config_path=empty_config_path, repeatable=True) as d2:
            r_with = d2.classify_file(with_pos)[0]
            r_without = d2.classify_file(without_pos)[0]

        assert abs(r_with.raw.NEO - r_without.raw.NEO) > 0.5

    def test_manual_observation_earth_obs(self, model_path, obscodes_path,
                                          empty_config_path):
        """Setting spacebased/earth_obs directly on Observations must reach
        the scoring engine (previously dropped by to_tuple/_extension).

        Uses the same tracklet as the XML tests so the expected score
        shift is the same.
        """
        from digest2.observation import _iso_to_mjd

        def _tracklet(spacebased):
            return [
                Observation(mjd=_iso_to_mjd(t), ra=ra, dec=dec,
                            mag=mag, obscode="C58",
                            spacebased=spacebased,
                            earth_obs=([p * _KM_TO_AU for p in pos]
                                       if spacebased else [0.0, 0.0, 0.0]))
                for (t, ra, dec, mag, pos) in SAT_OBS
            ]

        with Digest2(model_path=model_path, obscodes_path=obscodes_path,
                     config_path=empty_config_path, repeatable=True) as d2:
            r_space = d2.classify_tracklet(_tracklet(True))
            r_geo = d2.classify_tracklet(_tracklet(False))

        assert abs(r_space.raw.NEO - r_geo.raw.NEO) > 2.0

    def test_repeatable_satellite_scores(self, tmp_path, model_path,
                                         obscodes_path, empty_config_path):
        path = _write_sat_xml(tmp_path / "sat.xml")
        with Digest2(model_path=model_path, obscodes_path=obscodes_path,
                     config_path=empty_config_path, repeatable=True) as d2:
            r1 = d2.classify_file(path)[0]
            r2 = d2.classify_file(path)[0]
        assert r1.raw.NEO == r2.raw.NEO
        assert r1.noid.NEO == r2.noid.NEO

    def test_pinned_satellite_scores(self, tmp_path, model_path,
                                     obscodes_path, cli_config_path):
        """Pin the satellite tracklet scores (repeatable mode).

        Reference values from the C CLI (population model of 2026-06),
        which reads pos1/pos2/pos3:
            ST001aa  0.00  NEO 28 78  MB1 43 29
        The geocentric (bugged) scores were NEO 36 79, MB1 37 18.
        """
        path = _write_sat_xml(tmp_path / "sat.xml")
        with Digest2(model_path=model_path, obscodes_path=obscodes_path,
                     config_path=cli_config_path, repeatable=True) as d2:
            r = d2.classify_file(path, classes=["NEO", "MB1"])[0]

        assert round(r.raw.NEO) == 28
        assert round(r.noid.NEO) == 78
        assert round(r.raw.MB1) == 43
        assert round(r.noid.MB1) == 29


# ---------------------------------------------------------------------------
# C CLI parity (skip when the binary is not built)
# ---------------------------------------------------------------------------
class TestCliParity:

    def _compare(self, cli_scores, result, tolerance):
        """Compare CLI-rounded scores against Python floats."""
        rms, neo_raw, neo_noid, mb1_raw, mb1_noid = cli_scores
        assert abs(result.rms - rms) < 0.1
        assert abs(result.raw.NEO - neo_raw) <= tolerance
        assert abs(result.noid.NEO - neo_noid) <= tolerance
        assert abs(result.raw.MB1 - mb1_raw) <= tolerance
        assert abs(result.noid.MB1 - mb1_noid) <= tolerance

    def test_satellite_xml_matches_cli(self, tmp_path, model_path,
                                       obscodes_path, cli_config_path):
        path = _write_sat_xml(tmp_path / "sat.xml")
        proc = _cli(["-c", cli_config_path, path])
        assert proc.returncode == 0, proc.stderr
        cli_scores = _parse_cli_scores(proc.stdout)["ST001aa"]

        with Digest2(model_path=model_path, obscodes_path=obscodes_path,
                     config_path=cli_config_path, repeatable=True) as d2:
            r = d2.classify_file(path, classes=["NEO", "MB1"])[0]

        # CLI prints rounded integers; the XML date conversion differs in
        # the last ULP, so allow slightly more than rounding error.
        self._compare(cli_scores, r, tolerance=0.6)

    def test_satellite_obs80_matches_cli(self, tmp_path, model_path,
                                         obscodes_path, cli_config_path):
        path = _write_sat_obs80(tmp_path / "sat.obs")
        proc = _cli(["-c", cli_config_path, path])
        assert proc.returncode == 0, proc.stderr
        cli_scores = _parse_cli_scores(proc.stdout)["K16S99K"]

        with Digest2(model_path=model_path, obscodes_path=obscodes_path,
                     config_path=cli_config_path, repeatable=True) as d2:
            r = d2.classify_file(path, classes=["NEO", "MB1"])[0]

        # The 80-column parser is bit-compatible with the C parser, so
        # only CLI display rounding separates the two outputs.
        self._compare(cli_scores, r, tolerance=0.51)

    def test_cli_itself_uses_positions(self, tmp_path, cli_config_path):
        """Sanity check on the reference implementation: the CLI's scores
        must change when pos1/pos2/pos3 are removed."""
        with_pos = _write_sat_xml(tmp_path / "sat.xml")
        without_pos = _write_sat_xml(tmp_path / "nopos.xml", with_pos=False)

        r1 = _cli(["-c", cli_config_path, with_pos])
        r2 = _cli(["-c", cli_config_path, without_pos])
        assert r1.returncode == 0, r1.stderr
        assert r2.returncode == 0, r2.stderr

        s1 = _parse_cli_scores(r1.stdout)["ST001aa"]
        s2 = _parse_cli_scores(r2.stdout)["ST001aa"]
        assert s1 != s2
