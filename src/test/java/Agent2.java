
import java.util.ArrayList;
import java.util.Scanner;


import java.io.File;
import java.io.FileNotFoundException;



public class Agent2 {
	
	static int agentNum = 2;
	
	public static ArrayList<Integer> readFromFile(String inputPath) {
		ArrayList<Integer> config = new ArrayList<>();
		try {
			File configFile = new File(inputPath);
			Scanner reader = new Scanner(configFile);
			String[] str_config = reader.nextLine().split(", ");
			
			for(String i : str_config) {
				config.add(Integer.parseInt(i));
			}
			
			reader.close();
			
		} catch (FileNotFoundException e) {
			System.err.println("Error: while reading config file");
			System.err.println(e);
		}
		
		return config;
	}
	
	static dPoint getVector(Point a, Point b) {
    	
		dPoint result = new dPoint(b.x-a.x,b.y-a.y);
    	
    	return result;
	}
    
    static dPoint normalizeVector(dPoint a) {
    	
    	double magnitude = Math.sqrt(Math.pow(a.x, 2) + Math.pow(a.y, 2));
    	

    	dPoint result = new dPoint((double) a.x/magnitude, (double) a.y/magnitude);
    	
    	return result;
    }
    
    static dPoint rotate(Point origin, dPoint destiny, double angle) {
    	    	
    	double qx = origin.x + (Math.cos(angle) * (destiny.x - origin.x)) - (Math.sin(angle) * (destiny.y - origin.y));
    	double qy = origin.y + (Math.sin(angle) * (destiny.x - origin.x)) + (Math.cos(angle) * (destiny.y - origin.y));
    	
    	dPoint result = new dPoint(qx, qy);
    	
    	return result;
    }
    
    static dPoint magnify(dPoint vector,double magnitude) {   	
    	dPoint result = new dPoint(vector.x * magnitude, vector.y * magnitude);
    	
    	return result;
    }
    
    static Point addVectors(Point first_checkpoint, dPoint b) {
    	Point result = new Point((int) Math.round(first_checkpoint.x + b.x), (int) Math.round(first_checkpoint.y + b.y));
    	return result;
    }
    
    private static class dPoint{
        public double x, y;
        
        public dPoint(double x, double y){
            this.x = x;
            this.y = y;
        }
    }
    
    
	
    private static class Point{
        public int x, y;
        
        public Point(int x, int y){
            this.x = x;
            this.y = y;
        }
        
        double distance(Point p) {
            return Math.sqrt((this.x - p.x) * (this.x - p.x) + (this.y - p.y) * (this.y - p.y));
        }
    }
	
    // This agent slows down from 200 to 50 when is at 4000 units before reaching the checkpoint
    public static void main(String[] args) throws Exception {
        // TODO Change var for each copy
        String filename = "ag"+agentNum;

        Scanner scanner = new Scanner(System.in);
        int checkpoints = Integer.parseInt(scanner.nextLine());
        ArrayList<Point> targets = new ArrayList<>();
        for(int i = 0; i < checkpoints; i++){
            String[] line = scanner.nextLine().split(" ");
            System.err.println(line[0] + " " + line[1]);
            targets.add(new Point(Integer.parseInt(line[0]), Integer.parseInt(line[1])));
        }
        double dist = 100000.0;
        int z = 0;
    	
        // Agent path for its configuration in project
    	ArrayList<Integer> config = readFromFile("src/test/java/individuals_configurations/" + filename + ".txt");
        
    	// TODO Implements config[index] for each parameter in rules
        
    	while (true) {
            String s = scanner.nextLine();
            System.err.println(s);
            String[] input = s.split(" ");
            // id x y vx vy angle
            int target = Integer.parseInt(input[0]);
            int x = Integer.parseInt(input[1]);
            int y = Integer.parseInt(input[2]);
            int vx = Integer.parseInt(input[3]);
            int vy = Integer.parseInt(input[4]);
            Point first_checkpoint = targets.get(target);
            //Point second_checkpoint = targets.get((target + 1) % targets.size());  // Target immediately after the intended

            Point current = new Point(x, y);
            
            // AGENT LOGIC
            
            // Parameters we control
            double default_thrust = config.get(0);  // 200
            double slow_down_limit_1 = config.get(1);  // 3000
            double slow_down_thrust_1 = config.get(2);  // 50
            double slow_down_thrust_1_coeff = config.get(3);  // 0.9
            double magnify_offset = config.get(4);  // 10 This must be adjusted depending on the value of the angles
            
            
            // LOGIC
            
            // Let's first determine the offset point to which we want to aim
            dPoint dir_current_first = getVector(first_checkpoint, current);
            dPoint normed = normalizeVector(dir_current_first);
            dPoint rotated = rotate(first_checkpoint, normed, 90);
            dPoint magnified = magnify(rotated, magnify_offset);
            Point offset_point = addVectors(first_checkpoint, magnified);
            
            
            double thrust = default_thrust;
            if(first_checkpoint.distance(current) < slow_down_limit_1){
                thrust = slow_down_thrust_1;
            }
            System.out.println(first_checkpoint.x + " " + first_checkpoint.y + " " + (int) thrust + " Agent " + agentNum); // X Y THRUST MESSAGE
        }
    }
}
