import java.io.FileOutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
//import org.json.simple.JSONObject;

import com.codingame.gameengine.runner.SoloGameRunner;
import com.codingame.gameengine.runner.dto.GameResult;



public class SkeletonMain {
	
    public static void main(String[] args) {
        // Uncomment this section and comment the other one to create a Solo Game
    	int train = 3;
    	
    	ArrayList<Integer> timeResults = new ArrayList<>();
    	ArrayList<ArrayList<Integer>> diffResults = new ArrayList<>();
    	
//    	for (int i = 0; i < 1; i++) {
    	for (int i = 0; i < train; i++) {
    		/* Solo Game */
    		SoloGameRunner gameRunner = new SoloGameRunner();
    		// Sets the player
    		gameRunner.setAgent(Agent1.class);
    		// Sets a test case
    		gameRunner.setTestCase("test"+ Integer.toString(i) +".json");
    		
    		// Another way to add a player for python
    		// gameRunner.addAgent("python3 /home/user/player.py");
    		
    		// Start the game server
    		// gameRunner.start();
    		// Simulate
    		GameResult gr = gameRunner.simulate();
    		
    		timeParser(timeResults, gr);
    		stepsParser(diffResults, gr);
    		
    	}
    	
    	saveResults(timeResults, diffResults);
    	
    	
    }

    /** Gets experiments results, storing it in a HashMap. Later it rewrite it to save in a json file
     * 
     * @param timeResults
     * @param diffResults
     */
	private static void saveResults(ArrayList<Integer> timeResults, ArrayList<ArrayList<Integer>> diffResults) {
		HashMap<String, Object> gameResults = new HashMap<>();
    	gameResults.put("times", timeResults);
    	gameResults.put("steps", diffResults);
    	try {
			FileOutputStream fos = new FileOutputStream("src/test/java/experiments/Agent1.json");
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
	private static void timeParser(ArrayList<Integer> timeResults, GameResult gameResult) {
		String time = gameResult.metadata;
		String[] time_splited = time.substring(1, time.length()-2).split(":");
		time_splited[1] = time_splited[1].substring(1, time_splited[1].length()-2);
		timeResults.add((int) (Float.parseFloat(time_splited[1])));
	}
    
    
}
