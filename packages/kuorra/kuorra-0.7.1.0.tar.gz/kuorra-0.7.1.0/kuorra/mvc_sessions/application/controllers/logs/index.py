import config


class Index:

    def GET(self):
        result = config.model.get_all_logs().list()
        for row in result:
            row.id_log = config.make_secure_val(str(row.id_log))
        return config.render.index(result)