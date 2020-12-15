# Heritage

##  Created by Joshua Anderson

You are a small medieval town that is trying to survive in a harsh world. You have famers, scientists, artists, and knights. You must make decisions to best grow your society trading off hunger, technological advancement, happiness, and military power. You must keep your people fed or your town will not be able to grow! Through research you may find ways to more efficiently produce food or stronger weapons for fighting! If your people are not happy enough, they will leave the town! With a strong military, you can keep your farms well guarded! Seems easy, right? Well there are other towns as well trying to accomplish the same goal. The difference is they are smart and pass down a stronger generation as the game progresses. If you aren't too careful, they might conquer you!

## How to Play

### Running Heritage

To run the game, you must have Python 3.x installed. Only default libraries are used. To start playing run the following in the console while in the main directory of the repository:

```bash
python HeritageGame.py
```

There will be options to quit the game through the menu of the player's turn and at the main menu.

### Rules of the Game

#### Beginning the game

You will start by creating the settings for your game like the name of your village and the number of AI you will be playing against. You then will be asked to divide 20 villagers into four roles:

- **farmer:** farmers produce 1.5 wheat by default
- **artist:** artists produce 1.5 happiness by default
- **scientist:** scientists produce 1.5 research by default
- **knight:** knights have 1.5 strength by default

Each village has the option to attack or grow. A village must have at least five knights to attack and victory will be determined by the difference in strength of the two villages. If a village decides to grow, they choose one role to assign the villager to.

#### Production and Usage

Each member of the population will consume 1 wheat and *p* / 3 happiness where p is the size of the population.

Scientists will find a scientific breakthrough at a rate of: 10 * 3<sup>x</sup> with a starting *x* of 0.

#### Goal

Each village is trying to conquer the entire country by being the last to survive. A village dies if their population reaches 0. If the player dies, the simulation will end. If all the other villages die off, the player will win.

## Breaking Down the AI

**Note:** Option 2 of the main menu offers a brief walkthrough of how the AI makes decisions.

### Pseudo Code of AI Turn

```python
if isAlive
    roll die (1/10 chance of attack)
    if attack and knights >= 5
        attack()
    else
        grow()
else
    no turn
```

### Predicting Player Moves

I used weighted predictions with bayesian priors and updating. A prior consists of four keys mapped to an integer value. For example:

```python
priors = {'farmers': 5, 'artists': 4, 'scientists': 1, 'knights': 10}
```

The integers represent the assumed population for the player by the AI. In the example of the Empire Archetype, it assumes the player will start with 5 farmers, 4 artists, 1 scientist, and 10 knights. 

The priors are used to calculate the weight of a given role. The main assumption behind the equation is that the player will choose the least populated role given the assumed population. Here is the equation:

```python
sum(priors.values()) / prior_i
```

In this example, the weights for predicting the player's move would be:
```python
weights = {'farmers': 4, 'artists': 5, 'scientists': 20, 'knights': 2}
```

The predicted move would be scientists. 

When the player makes a move, the priors are updated accordingly. This is done by increasing the role the player grew by one. For example if the player were to grow with a scientist, the new priors would be:

```python
priors = {'farmers': 5, 'artists': 4, 'scientists': 2, 'knights': 10}
```

### Countering Player moves

Once the AI predicts the player move using the method above, it attempts to counter it These are the AI counters for each role:

<table>
    <thead>
        <tr>
            <th>Player Move</th>
            <th>Counter</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>farmer</td>
            <td>farmer</td>
        </tr>
        <tr>
            <td>artist</td>
            <td>artist</td>
        </tr>
        <tr>
            <td>scientist</td>
            <td>knight</td>
        </tr>
        <tr>
            <td>knight</td>
            <td>scientist</td>
        </tr>
    </tbody>
</table>

Since our example predicts the player will play a scientist, it will choose knight for growth.

The reasoning for the counters is as follows: producers should match producers, advancing technology gives a long-term advantage over strength, and strength gives a short-term advantage over technology. 

### Psuedo Code for AI Growth
```python
# prioritize obtaining positive net production
if wheat production < wheat consumption
    grow(farmer)
else if happiness productino < art production
    grow(artist)
# otherwise counter player move
else
    predicted_move = predict()
    counter_move = counter(predicted_move)
    grow(counter_move)
```

### Archetypes

There are five preset archetypes for the AI: Empire, Kingdom, Valley, Monastery, and Grasslands.

Each of these archetypes has different attributes at the start of the game, changing how they will play. Here is a reference table of the different values for each preset:

<table>
    <thead>
        <tr>
            <th>Archetype</th>
            <th>Villager Role</th>
            <th>Inital Population</th>
            <th>Inital Priors</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=8>Empire</td>
            <td rowspan=2>Farmer</td>
        </tr>
        <tr>
            <td>8</td>
            <td>5</td>
        </tr>
        <tr>
            <td rowspan=2>Artist</td>
        </tr>
        <tr>
            <td>2</td>
            <td>4</td>
        </tr>
        <tr>
            <td rowspan=2>Scientist</td>
        </tr>
        <tr>
            <td>2</td>
            <td>1</td>
        </tr>
        <tr>
            <td rowspan=2>Knight</td>
        </tr>
        <tr>
            <td>8</td>
            <td>10</td>
        </tr>
                <tr>
            <td rowspan=8>Grasslands</td>
            <td rowspan=2>Farmer</td>
        </tr>
        <tr>
            <td>15</td>
            <td>7</td>
        </tr>
        <tr>
            <td rowspan=2>Artist</td>
        </tr>
        <tr>
            <td>5</td>
            <td>5</td>
        </tr>
        <tr>
            <td rowspan=2>Scientist</td>
        </tr>
        <tr>
            <td>0</td>
            <td>4</td>
        </tr>
        <tr>
            <td rowspan=2>Knight</td>
        </tr>
        <tr>
            <td>0</td>
            <td>4</td>
        </tr>
                <tr>
            <td rowspan=8>Monastery</td>
            <td rowspan=2>Farmer</td>
        </tr>
        <tr>
            <td>10</td>
            <td>5</td>
        </tr>
        <tr>
            <td rowspan=2>Artist</td>
        </tr>
        <tr>
            <td>10</td>
            <td>4</td>
        </tr>
        <tr>
            <td rowspan=2>Scientist</td>
        </tr>
        <tr>
            <td>0</td>
            <td>7</td>
        </tr>
        <tr>
            <td rowspan=2>Knight</td>
        </tr>
        <tr>
            <td>0</td>
            <td>4</td>
        </tr>
                <tr>
            <td rowspan=8>Valley</td>
            <td rowspan=2>Farmer</td>
        </tr>
        <tr>
            <td>8</td>
            <td>5</td>
        </tr>
        <tr>
            <td rowspan=2>Artist</td>
        </tr>
        <tr>
            <td>3</td>
            <td>5</td>
        </tr>
        <tr>
            <td rowspan=2>Scientist</td>
        </tr>
        <tr>
            <td>7</td>
            <td>3</td>
        </tr>
        <tr>
            <td rowspan=2>Knight</td>
        </tr>
        <tr>
            <td>2</td>
            <td>7</td>
        </tr>
                <tr>
            <td rowspan=8>Kingdom</td>
            <td rowspan=2>Farmer</td>
        </tr>
        <tr>
            <td>5</td>
            <td>5</td>
        </tr>
        <tr>
            <td rowspan=2>Artist</td>
        </tr>
        <tr>
            <td>5</td>
            <td>5</td>
        </tr>
        <tr>
            <td rowspan=2>Scientist</td>
        </tr>
        <tr>
            <td>5</td>
            <td>5</td>
        </tr>
        <tr>
            <td rowspan=2>Knight</td>
        </tr>
        <tr>
            <td>5</td>
            <td>5</td>
        </tr>
    </tbody>
</table>

### Comparing Algorithm to Alternatives

To divide up my reflection on the pros and cons of each potential algorithm, I compiled this table:

<table>
    <thead>
        <tr>
            <th>Algorithm</th>
            <th></th>
            <th>Reflection</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=4>Bayesian Updating</td>
            <td rowspan=2>Pros</td>
        </tr>
        <tr>
            <td>The main assumptions of this algorithm are that the player will always choose the smallest populated role and will have a specific starting population. The benefit of this is that the assumption that the player will generally choose an area they are lacking (ignoring the constraint of net production). Also depending on the priors, the algorithm will quickly learn what roles the player prioritizes. With that information, it can in time make fairly accurate predictions of what the player's next move will be and counter it. With accurate priors, a given village will challenge the player well.</td>
        </tr>
        <tr>
            <td rowspan=2>Cons</td>
        </tr>
        <tr>
            <td>The main issue with this algorithm is it is very reactive to the player's decisions and may not always take into account the best strategy for its own growth. If the player does not prioritize strength or technology, neither will the algorithm and will make the village inheriently weak to other AI unless it was given a knight or science heavy starting population. If it does not have a desirable starting population, it will likely fail despite however accurately it can counter the player moves. Additionally it is extremely computationally light in that it only has a few calculations to make all with time complexity of O(1).</td>
        </tr>
        <tr>
            <td rowspan=4> Multi-Population Genetic Algorithm</td>
            <td rowspan=2>Pros</td>
        </tr>
        <tr>
            <td>If the strategy of the GA consisted of optimal moves for 100 turns, the AI would thrive at growing a strong village. It would be able to optimize the choice of growing each role on a given turn. This would make the AI much more difficult to attack as the player as the algorithm would likely be making much better decisions on a turn by turn basis.</td>
        </tr>
        <tr>
            <td rowspan=2>Cons</td>
        </tr>
        <tr>
            <td>There are two main issues with this algorithm. The first being that it would be extremely computationally heavy. A single AI would need to run likely at least 1000 generations. Each generation would consist of a list of a population of at least 100 strategies (each a list of length 100). Each generation would also have a number of O(n) calculations to manipulate the stratigies it carries. That would then be multiplied by the number of AI the player chooses to play against. This brings me to the next issue, the variability of the optimal solution. Every time the AI gets attacked, or attacked, the optimal solution would change and the algorithm would have to recalculate. This again, would add to the time and space complexity of the algorithm</td>
        </tr>
        <tr>
            <td rowspan=4>Linear Programming</td>
            <td rowspan=2>Pros</td>
        </tr>
        <tr>
            <td>With the nature of the game, there are a number of constraints that need to be taken into account. Linear programming would offer much simpler code that could produce just as good results. Alternative to the genetic algorithm, this algorithm would be good at finding an optimal solution for the given turn and would adapt each turn rather than produce a solution for an entire game. This would also allow for a more complex and constrained environment without adding too much complexity to the code. This means adding any future rules to the game would be made simpler.</td>
        </tr>
        <tr>
            <td rowspan=2>Cons</td>
        </tr>
        <tr>
            <td>An issue with this algorithm would be that the solution to finding the optimal strategy to the game is not a linear problem. It would take more time and effort to think about how to make the problem into a linear problem to then implement in code. </td>
        </tr>
    </tbody>
</table>