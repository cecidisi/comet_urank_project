class UpmcStudyRouter(object): 
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'upmc_study':
            return 'upmcevaldb'
        return None

    def db_for_write(self, model, **hints):
        # "Point all operations on conf_navigator models to 'conf_navigator'"
        if model._meta.app_label == 'upmc_study':
            return 'upmcevaldb'
        return False
    
    def allow_relation(self, obj1, obj2, **hints):
        # "Allow any relation if a both models in the same app"
        if obj1._meta.app_label == 'upmc_study' or obj2._meta.app_label == 'upmc_study':
            return True
        return None
    
    def allow_syncdb(self, db, model):
        if db == 'upmcevaldb':
            return model._meta.app_label == 'upmc_study'
        elif model._meta.app_label == 'upmc_study':
            return False
        return None


