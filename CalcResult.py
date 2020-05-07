
class ResultRow:
    def __init__(self, _range, path, moa, time, windage, windage_moa, velocity):
        self.range = _range
        self.path = path
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
    def __init__(self, rows=[]):
        self.rows = []
        for row in rows:
            self.add_row(*row)
    
    def add_row(self, _range, path, moa, time, windage, windage_moa, velocity):
        self.rows.append(ResultRow(_range, path, moa, time, windage, windage_moa, velocity))