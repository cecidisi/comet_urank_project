class CometRouter(object): 
    def db_for_read(self, model, **hints):
        # "Point all operations on comet_urank models to 'cometdb'"
        # print hints
        if model._meta.app_label == 'comet_urank':
            return 'cometdb'
        return None

    def db_for_write(self, model, **hints):
        # "Point all operations on comet_urank models to 'comet_urank'"
        if model._meta.app_label == 'comet_urank':
            return 'cometdb'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        # "Allow any relation if a both models in the same app"
        if obj1._meta.app_label == 'comet_urank' and obj2._meta.app_label == 'comet_urank':
            return True
        return None
    
    def allow_syncdb(self, db, model):
        if db == 'cometdb':
            return model._meta.app_label == 'comet_urank'
        return None