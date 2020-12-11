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
attack_fail = "were captured in battle"
attack_success = "were recruited during the attack"
default_tech = 1.5

AI_names = ["Apollo", "Arthur", "Augustine", "Bernard", "Cid", "Constantine", "Dante",
            "Euripides", "Fuller", "Garnet", "Hector", "Isa", "Issabell", "Eve",
            "Joanna", "Madlyn", "Roysa"]
AI_counters = {"farmer": "farmer", "artist": "artist", "scientist": "knight", "knight": "scientist", "none": "none"}
AI_attack_freq = 0.1

def game_desc(line_ending):
    return ("You have famers, scientists, artists, and knights. You must make decisions to best" +
            " grow your society trading off hunger, technological advancement, happiness, and military power." + line_ending +
            "You must keep your people fed or your village will not be able to grow! Through research you may" +
            " find ways to more efficiently produce food, better amenities, or stronger weapons for fighting!" + line_ending +
            "If your people are not happy enough, they will leave the village! With a strong military," +
            " you can keep your farms well guarded!" + line_ending + "Seems easy, right? Well there are other villages as well" +
            " trying to accomplish the same goal. The difference is they are smart and pass down a stronger" +
            " generation as the game progresses." + line_ending + "If you aren't too careful, they might conquer you!")

def turn_info(line_ending):
    return("Every year the following will happen, and you will make a decision about how to proceed for the next year:" + line_ending + line_ending +
        "\t- Our scouts will inform us of other villages' population." + line_ending +
        "\t- I personally will be sending you messages about updates around the village to keep you aware of how our people are doing." + line_ending +
        "\t- A new child will grow old enough to join the workforce. You may decide to give them a role or let them be." + line_ending +
        "\t- Alternatively, you may need the time to plan an attack another village which if successful, will be a great source of food, art, science, and new workers." + line_ending +
        "\t- We cannot attack the same village twice in a row." + line_ending + 
        line_ending + "That is everything! Good luck!" + line_ending)