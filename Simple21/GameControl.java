package simple21;

import java.util.*;

/**
 * This is a simplified version of a common card game, "21". 
 */
public class GameControl {
    
	/**
	 * Human player.
	 */
    HumanPlayer human;
    
    /**
     * Computer player.
     */
    ComputerPlayer player1;
    
    /**
     * Computer player.
     */
    ComputerPlayer player2;
    
    /**
     * Computer player.
     */
    ComputerPlayer player3;
    
    /** 
     * A random number generator to be used for returning random "cards" in a card deck.
     * */
    Random random = new Random();
      
    /**
     * The main method just creates a GameControl object and calls its run method.
     * @param args Not used.
     */
    public static void main(String args[]) {    
        new GameControl().run();
    }
    
    /**
     * Prints a welcome method, then calls methods to perform each of the following actions:
     * - Create the players (one of them a Human)
     * - Deal the initial two cards to each player
     * - Control the play of the game
     * - Print the final results
     */
    public void run() {
    	
        Scanner scanner = new Scanner(System.in);
        // Students: your code goes here.
        System.out.println("Welcome to Simple 21!\n" +
                "You'll play against 3 other players (computers).\n" +
                "Try to get as close to 21 as possible, without going over.\n" +
                "What is your name?");
        String humansName = scanner.next();

    	this.createPlayers(humansName);
        this.deal();
        this.controlPlay(scanner);
        this.printResults();
        
        scanner.close();
    }
    
    /**
     * Creates one human player with the given humansName, and three computer players with hard-coded names.
     * @param humansName for human player
     */
    public void createPlayers(String humansName) {
       // Students: your code goes here.
       // Create players
       this.human = new HumanPlayer(humansName);
       this.player1 = new ComputerPlayer("Player1");
       this.player2 = new ComputerPlayer("Player2");
       this.player3 = new ComputerPlayer("Player3");
    }
    
    /**
     * Deals two "cards" to each player, one hidden, so that only the player who gets it knows what it is, 
     * and one face up, so that everyone can see it. (Actually, what the other players see is the total 
     * of each other player's cards, not the individual cards.)
     */
    public void deal() { 
        // Students: your code goes here.
    	human.takeVisibleCard(nextCard());
        human.takeHiddenCard(nextCard());

        player1.takeVisibleCard(nextCard());
        player1.takeHiddenCard(nextCard());
        
        player2.takeVisibleCard(nextCard());
        player2.takeHiddenCard(nextCard());

        player3.takeVisibleCard(nextCard());
        player3.takeHiddenCard(nextCard());
    }
    
    /**
     * Returns a random "card", represented by an integer between 1 and 10, inclusive. 
     * The odds of returning a 10 are four times as likely as any other value (because in an actual
     * deck of cards, 10, Jack, Queen, and King all count as 10).
     * 
     * Note: The java.util package contains a Random class, which is perfect for generating random numbers.
     * @return a random integer in the range 1 - 10.
     */
    public int nextCard() { 
    	// Students: your code goes here.
    	int possibility = random.nextInt(13) + 1;
        // JQK
        if (possibility >= 11) return 10;
        // 1 - 10
        return random.nextInt(9) + 1;
    }

    /**
     * Gives each player in turn a chance to take a card, until all players have passed. Prints a message when 
     * a player passes. Once a player has passed, that player is not given another chance to take a card.
     * @param scanner to use for user input
     */
    public void controlPlay(Scanner scanner) { 
        // Students: your code goes here.
    	while(!checkAllPlayersHavePassed()){
            if(!human.passed){
                if(human.offerCard(human, player1, player2, player3, scanner)){
                    human.takeVisibleCard(nextCard());
                }
                else{
                    System.out.println(human.name + " passes." );
                }
            }

            if(!player1.passed){
                if(player1.offerCard(human, player1, player2, player3)){
                    player1.takeVisibleCard(nextCard());
                }
                else{
                    System.out.println(player1.name + " passes." );
                }
            }

            if(!player2.passed){
                if(player2.offerCard(human, player1, player2, player3)){
                    player2.takeVisibleCard(nextCard());
                }
                else{
                    System.out.println(player2.name + " passes." );
                }
            }

            if(!player3.passed){
                if(player3.offerCard(human, player1, player2, player3)){
                    player3.takeVisibleCard(nextCard());
                }
                else{
                    System.out.println(player3.name + " passes." );
                }
            }
        }
    }
     
    /**
     * Checks if all players have passed.
     * @return true if all players have passed
     */
    public boolean checkAllPlayersHavePassed() {
    	// Students: your code goes here.
    	return human.passed && player1.passed && player2.passed && player3.passed;
    }
    
    /**
     * Prints a summary at the end of the game.
     * Displays how many points each player had, and if applicable, who won.
     */
    public void printResults() { 
        // Students: your code goes here.
        System.out.println();
    	System.out.println("Game Over.");
        System.out.println(human.name + " has " + human.getScore() + " total point(s).");
        System.out.println(player1.name + " has " + player1.getScore() + " total point(s).");
        System.out.println(player2.name + " has " + player2.getScore() + " total point(s).");
        System.out.println(player3.name + " has " + player3.getScore() + " total point(s).");
        printWinner();
    }

    /**
     * Determines who won the game, and prints the results.
     */
    public void printWinner() { 
        // Students: your code goes here.
    	HashMap<String, Integer> finalScore = new HashMap<>();
        finalScore.put(human.name, human.getScore());
        finalScore.put(player1.name, player1.getScore());
        finalScore.put(player2.name, player2.getScore());
        finalScore.put(player3.name, player3.getScore());

        int maxScore = 0;
        Object name = "";
        int tie = 0;

        // inspect the scores
        for(int score: finalScore.values()){
            // score should be at most 21
            if (score < 22){
                if (maxScore < score){
                    // replace the maxScore with the current score
                    maxScore = score;
                }
                else if (maxScore == score){
                    // several players have the same score
                    tie += 1;
                }
            }
        }
        // players hold different value and there is a maxScore < 21
        if (tie == 0 && maxScore != 0){
            for (Map.Entry entry: finalScore.entrySet()){
                if (entry.getValue().equals(maxScore)){
                    name = entry.getKey();
                    System.out.println(name + " wins with " + maxScore + " point(s).");
                }
            }
        }
        // several players hold the same value and there is a maxScore < 21
        else if (tie != 0 && maxScore != 0){
            System.out.println("It's a tie. Nobody wins.");
        }
        // all scores exceed 21
        else{
            System.out.println("Nobody wins.");
        }
    }
}
