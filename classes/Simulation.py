from classes.Village import *


class HeritageGame:
    def __init__(self, init_pop):
        self.population_size = init_pop

    def main_menu(self):
        line_ending = "\n"
        title = """                                                                                           
     *****    **                                                                                
  ******  *  **** *                          *         *                                        
 **   *  *   *****                          ***       **                                        
*    *  *    * *                             *        **                                        
    *  *     *                ***  ****             ********                                    
   ** **     *         ***     **** **** * ***     ********     ****        ****         ***    
   ** **     *        * ***     **   ****   ***       **       * ***  *    *  ***  *    * ***   
   ** ********       *   ***    **           **       **      *   ****    *    ****    *   ***  
   ** **     *      **    ***   **           **       **     **    **    **     **    **    *** 
   ** **     **     ********    **           **       **     **    **    **     **    ********  
   *  **     **     *******     **           **       **     **    **    **     **    *******   
      *       **    **          **           **       **     **    **    **     **    **        
  ****        **    ****    *   ***          **       **     **    **    **     **    ****    * 
 *  *****      **    *******     ***         *** *     **     ***** **    ********     *******  
*     **              *****                   ***              ***   **     *** ***     *****   
*                                                                                ***            
 **                                                                        ****   ***           
                                                                         *******  **            
                                                                        *     ****"""
        print(title)
        print()
        print("Welcome settler! Prepare to breed generations of your village stronger than any other!")
        print()
        print("You have famers, scientists, artists, and knights. You must make decisions to best" +
              " grow your society trading off hunger, technological advancement, happiness, and military power." + line_ending +
              "You must keep your people fed or your village will not be able to grow! Through research you may" +
              " find ways to more efficiently produce food or stronger weapons for fighting!" + line_ending +
              "If your people are not happy enough, they will leave the village! With a strong military," +
              " you can keep your farms well guarded!" + line_ending + "Seems easy, right? Well there are other villages as well" +
              "trying to accomplish the same goal. The difference is they are smart and pass down a stronger" +
              " generation as the game progresses." + line_ending + "If you aren't too careful, they might conquer you!")
