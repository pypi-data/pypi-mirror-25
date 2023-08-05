import logging,types

l = logging.getLogger(__name__)

class Utils():
    myconf = []



    @classmethod
    def config(cls,config,prefix=None,defaultval = None):
        if not prefix:
            prefix = cls.__name__.lower()
        for k in cls.myconf:
            if isinstance(k, types.StringTypes):
                prop = k
                key = prefix+"."+k
                default = defaultval
            else:
                try:
                    prop = k[0]
                    key = prefix+"."+k[0]
                    default = k[1]
                except:
                    continue
            setattr(cls,prop,config.get(key,default) )

            if key in config:
                l.debug("value of {key} set to: {val}".format(key=prop,val=config[key]))
                #setattr(cls,k,unicode(config[key]) ) 