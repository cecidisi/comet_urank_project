class UpmcUrankRouter(object): 
    def db_for_read(self, model, **hints):
        # "Point all operations on conf_navigator models to 'confnavdb'"
        # print '================ START'
        # print '@ conf_navigator'
        # print model._meta
        # print hints
        # print '================ END'
        if model._meta.app_label == 'upmc_urank':
            return 'upmcdb'
        return None

    def db_for_write(self, model, **hints):
        # "Point all operations on conf_navigator models to 'conf_navigator'"
        if model._meta.app_label == 'upmc_urank':
            return 'upmcdb'
        return False
    
    def allow_relation(self, obj1, obj2, **hints):
        # "Allow any relation if a both models in the same app"
        if obj1._meta.app_label == 'upmc_urank' or obj2._meta.app_label == 'upmc_urank':
            return True
        return None
    
    def allow_syncdb(self, db, model):
        if db == 'upmcdb':
            return model._meta.app_label == 'upmc_urank'
        elif model._meta.app_label == 'upmc_urank':
            return False
        return None


