'''
Don't pay any attention to this module, it is only present here for me to fiddle
with the tool while I'm developing it in my IDE
'''
import pynusmv_community.cmdline as cmdline
import pynusmv_community.main    as main
 
        
if __name__ == '__main__':
    #model= "NMH21_2"
    #path = "/Users/user/Documents/EXPERIMENTS/Modularite/models/nameche" 
    #prop = "G (v211.U_IR_01AM.st = l -> ((v211.P_01AM.posi = cdr ->  X v211.P_01AM.posi = cdr) & (v211.P_01AM.posi = cdn ->  X v211.P_01AM.posi = cdn)))"
    
    model = "abp4"
    path  = "/Users/user/Documents/EXPERIMENTS/Modularite/models"
    prop  = "(G F sender.state = get) & (G F receiver.state = deliver )"
    cmdline.__VERBOSE = True
    
    args     = cmdline.arguments().parse_args([
        '--path', path, '--formula', prop, '-k', '10', '-K', '10', #'-K', '100',
        '--weighted',
        #'--dump-raw-communities',
        #'--show-vig',
        #'--mine-patterns', 
        #'--mine-sequences',
        #'--show-cluster-graph',
        #'--dump-json-cluster-graph',
        #'--dump-stats',
        #'--show-stats',
        #'--show-d3-cluster-graph', ## kinda useless
        '--show-time-table',
        #'--show-formal-concepts',
        model
        ])
    
                                                                                  
    rng  = range(args.min_bound, 1+args.max_bound)
    main.process(args.path, args.model, args.formula, rng, args)
