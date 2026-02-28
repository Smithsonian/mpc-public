"""Observatory Codes API mixin."""

from ._compat import require_pandas


class ObscodesMixin:

    def get_observatory(self, obscode):
        """Get information about a specific observatory.

        Parameters
        ----------
        obscode : str
            Three-character observatory code (e.g. ``"500"``, ``"F51"``).

        Returns
        -------
        dict
            Observatory data including name, longitude, parallax constants.
        """
        return self._get("/api/obscodes", json={"obscode": obscode})

    def get_all_observatories(self):
        """Get information about all registered observatories.

        Returns
        -------
        dict
            Mapping of observatory code to observatory data.
        """
        return self._get("/api/obscodes", json={})

    def get_all_observatories_df(self):
        """Get all observatories as a pandas DataFrame.

        Returns
        -------
        pandas.DataFrame
            DataFrame indexed by observatory code.
        """
        pd = require_pandas()
        data = self.get_all_observatories()
        return pd.DataFrame.from_dict(data, orient="index")

    def search_observatories(self, name_pattern):
        """Search observatories by name (case-insensitive substring match).

        Parameters
        ----------
        name_pattern : str
            Substring to search for in observatory names.

        Returns
        -------
        pandas.DataFrame
            Matching observatories.
        """
        df = self.get_all_observatories_df()
        mask = df["name"].str.lower().str.contains(name_pattern.lower(), na=False)
        return df[mask]
