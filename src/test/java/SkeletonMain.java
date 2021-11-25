import java.io.FileOutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.codingame.gameengine.runner.SoloGameRunner;
import com.codingame.gameengine.runner.dto.GameResult;



public class SkeletonMain {
	
    public static void main(String[] args) {
        // Uncomment this section and comment the other one to create a Solo Game
    	int train = 1;
    	int agentNumber = Integer.parseInt(args[0]);
    	System.out.println("Entré");
		System.out.println(args[0]);

    	ArrayList<Float> timeResults = new ArrayList<>();
    	ArrayList<ArrayList<Integer>> diffResults = new ArrayList<>();

		// for (int i =0; i < 1 ; i++) {
		// 	i--;
		// }
    	boolean simulate = false;
    	
//    	for (int i = 0; i < 1; i++) {
    	for (int i = 0; i < train; i++) {
    		/* Solo Game */
    		SoloGameRunner gameRunner = new SoloGameRunner();
    		// Sets the player
    		Class<?> agentClass = setAgentClass(agentNumber);
    		gameRunner.setAgent(agentClass);
    		// Sets a test case
    		gameRunner.setTestCase("test"+ Integer.toString(i) +".json");
    		
    		// Another way to add a player for python
    		// gameRunner.addAgent("python3 /home/user/player.py");
    		
    		
    		// Simulate
    		if (simulate) { 
    			GameResult gr = gameRunner.simulate();
    			timeParser(timeResults, gr);
        		stepsParser(diffResults, gr);
    		} else {
    			// Start the game server
        		gameRunner.start();
    		}
    		
    		
    		
    	}
    	
    	if (simulate) { saveResults(agentNumber, timeResults, diffResults);}
    	
    	
    }

	private static Class<?> setAgentClass(int agentNumber) {
		Class<?> agentClass;
		try {
			agentClass = Class.forName("Agent" + agentNumber);
		} catch (ClassNotFoundException e) {
			System.err.println("Error: while loading class file");
			System.err.println(e);
			agentClass = Agent1.class;
		}
		return agentClass;
	}

    /** Gets experiments results, storing it in a HashMap. Later it rewrite it to save in a json file
     * 
     * @param timeResults
     * @param diffResults
     */
	private static void saveResults(int agentNumber, ArrayList<Float> timeResults, ArrayList<ArrayList<Integer>> diffResults) {
		HashMap<String, Object> gameResults = new HashMap<>();
    	gameResults.put("times", timeResults);
    	gameResults.put("steps", diffResults);
    	try {
			FileOutputStream fos = new FileOutputStream("src/test/java/experiments/ag" + agentNumber + ".json");
			fos.write(gameResults.toString().replaceAll("=", ":").replaceAll(":", "\":").replace("{", "{\"").replace(" s", " \"s")
					.getBytes());
			fos.flush();
			fos.close();
    	} catch (Exception e) {
			System.err.println("Error: while saving results file");
			System.err.println(e);
    	}
	}

	/** Extracts summaries from game results. It calculates tic's distances between successive checkpoints passed 
	 * 
	 * @param stepsResults
	 * @param gameResults
	 */
	private static void stepsParser(ArrayList<ArrayList<Integer>> stepsResults, GameResult gameResults) {
		List<String> spacesBetween = gameResults.summaries;
		ArrayList<Integer> steps = new ArrayList<>();
		int counter = 0;
		while (spacesBetween.get(counter).equals("")) {
			counter++;
		}
		int lastIndex = ++counter;
		
		while (counter < spacesBetween.size()) {
			if (!spacesBetween.get(counter).equals("")) {
				steps.add(counter - lastIndex);
				lastIndex = counter;
			}
			
			counter++;
		}
		
		stepsResults.add(steps);
	}

	/** Extracts metadata from game results. It reduces the String to time (integer)
	 * 
	 * @param timeResults
	 * @param mapNumber
	 * @param gameResult
	 */
	private static void timeParser(ArrayList<Float> timeResults, GameResult gameResult) {
		String time = gameResult.metadata;
		String[] time_splited = time.substring(1, time.length()-2).split(":");
		time_splited[1] = time_splited[1].substring(1, time_splited[1].length()-2);
		timeResults.add(Float.parseFloat(time_splited[1]));
	}
    
    
}
