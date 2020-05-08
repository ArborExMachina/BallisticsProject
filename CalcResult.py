
class ResultRow:
    def __init__(self, _range, path, moa, time, windage, windage_moa, velocity):
        self.range = _range     # x position in yards
        self.path = path        # y position in inches
        self.moa = moa
        self.time = time
        self.windage = windage
        self.windage_moa = windage_moa
        self.velocity = velocity        

    def tuple(self):
        return (
            self.range, 
            self.path,
            self.moa,
            self.time,
            self.windage,
            self.windage_moa,
            self.velocity
        )


class ResultTable:
    def __init__(self, params, rows=[]):
        self.params = params
        self.rows = []
        for row in rows:
            self.add_row(*row)
    
    def add_row(self, _range, path, moa, time, windage, windage_moa, velocity, filter=None):
        self.rows.append(ResultRow(_range, path, moa, time, windage, windage_moa, velocity))
    
    def find_maximal_peak(self, acceptable_threshold):
        peak = max(self.rows, key= lambda row: row.path)
        if peak.path > acceptable_threshold:
            return None
        return max(filter(lambda row: row.path == peak.path, self.rows), key=lambda row: row.range)