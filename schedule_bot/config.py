import optparse


class Config:
    TOKEN: str = ""
    OPW_TOKEN: str = ""

    @classmethod
    def read_opts(cls):
        opt = optparse.OptionParser()
        opt.add_option("-t", "--token", dest="token", default="")
        opt.add_option("--weather-api-token", dest="opw_token", default="")

        (opts, args) = opt.parse_args()
        cls.TOKEN = opts.token
        cls.OPW_TOKEN = opts.opw_token
