# -*- coding:utf-8 -*-
import pprint, cStringIO 


#任何格式的数据按utf-8打印出
class UniPrinter(pprint.PrettyPrinter):          
    def format(self, obj, context, maxlevels, level):  
        if isinstance(obj, unicode):  
            out = cStringIO.StringIO()  
            out.write('u"')  
            for c in obj:  
                if ord(c)<32 or c in u'"\\':  
                    out.write('\\x%.2x' % ord(c))  
                else:  
                    out.write(c.encode("utf-8"))  
                  
            out.write('"''"') 
            # result, readable, recursive 
            return out.getvalue(), True, False 
        elif isinstance(obj, str): 
            out = cStringIO.StringIO() 
            out.write('"')  
            for c in obj:  
                if ord(c)<32 or c in '"\\':  
                    out.write('\\x%.2x' % ord(c))  
                else:  
                    out.write(c)  
                  
            out.write('"')  
            # result, readable, recursive  
            return out.getvalue(), True, False  
        else:  
            return pprint.PrettyPrinter.format(self, obj,  
                context,  
                maxlevels,  
                level)          
