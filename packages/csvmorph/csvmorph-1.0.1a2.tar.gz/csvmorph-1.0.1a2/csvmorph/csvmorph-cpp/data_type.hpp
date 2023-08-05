/* Function for distinguishing numeric from text values
 */
 
# include <string>

namespace csvmorph {
    int data_type(std::string&);
    
    int data_type(std::string &in) {
        /*
        Returns:
            0:  If string
            1:  If int
            2:  If float
            
        Rules:
            - Leading and trailing whitespace ("padding") ignored
        */
        bool ws_allowed = true;
        
        for (int i = 0; i < in.size(); i++) {
        }
        
        return 2;
    }
}