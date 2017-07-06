class ConfNavigatorEvalRouter(object): 
    def db_for_read(self, model, **hints):
        # "Point all operations on conf_navigator models to 'confnavevaldb'"
        # print '================ START'
        # print '@ conf_navigator_EVAL'
        # print model._meta
        # print hints
        # print '================ END'
        
        if model._meta.app_label == 'conf_navigator_eval':
            return 'confnavevaldb'
        return None

    def db_for_write(self, model, **hints):
        # "Point all operations on conf_navigator models to 'conf_navigator'"
        if model._meta.app_label == 'conf_navigator_eval':
            return 'confnavevaldb'
        return False
    
    def allow_relation(self, obj1, obj2, **hints):
        # "Allow any relation if a both models in the same app"
        if obj1._meta.app_label == 'conf_navigator_eval' or obj2._meta.app_label == 'conf_navigator_eval':
            return True
        if obj1._meta.app_label == 'conf_navigator_eval' or obj2._meta.app_label == 'conf_navigator':
            return True
        if obj1._meta.app_label == 'conf_navigator' or obj2._meta.app_label == 'conf_navigator_eval':
            return True
        return None
    
    def allow_syncdb(self, db, model):
        if db == 'confnavevaldb':
            return model._meta.app_label == 'conf_navigator_eval'
        elif model._meta.app_label == 'conf_navigator_eval':
            return False
        return None


