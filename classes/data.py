import random

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

line_ending = "\n"
starve_str = "died of starvation"
unhappy_str = "left the village due to lack of happiness"
default_tech = 2

AI_names = ["Apollo", "Arthur", "Augustine", "Bernard", "Cid", "Constantine", "Dante",
            "Euripides", "Fuller", "Garnet", "Hector", "Isa", "Issabell", "Eve",
            "Joanna", "Madlyn", "Roysa"]

AI_counters = {"farmer": "farmer", "artist": "artist", "scientist": "knight", "knight": "scientist", "none": "none"}

def game_desc(line_ending):
    return ("You have famers, scientists, artists, and knights. You must make decisions to best" +
            " grow your society trading off hunger, technological advancement, happiness, and military power." + line_ending +
            "You must keep your people fed or your village will not be able to grow! Through research you may" +
            " find ways to more efficiently produce food, better amenities, or stronger weapons for fighting!" + line_ending +
            "If your people are not happy enough, they will leave the village! With a strong military," +
            " you can keep your farms well guarded!" + line_ending + "Seems easy, right? Well there are other villages as well" +
            " trying to accomplish the same goal. The difference is they are smart and pass down a stronger" +
            " generation as the game progresses." + line_ending + "If you aren't too careful, they might conquer you!")
