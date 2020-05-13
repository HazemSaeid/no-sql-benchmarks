from json import JSONEncoder

class CovidCase:
    def __init__(self, date, county, state, fips, cases, deaths):
        self.date = date
        self.county = county
        self.state = state
        self.fips = fips
        self.cases = cases
        self.deaths = deaths
class CovidCaseEncoder(JSONEncoder):
    def default(self,o):
        return o.__dict__