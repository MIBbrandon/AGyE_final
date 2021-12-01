
import java.util.ArrayList;
import java.util.Scanner;

import java.io.File;
import java.io.FileNotFoundException;



public class Agent1 {
	
	public static ArrayList<Double> readFromConfigFile(String inputPath) {
		ArrayList<Double> config = new ArrayList<>();
		try {
			File configFile = new File(inputPath);
			Scanner reader = new Scanner(configFile);
			String[] str_config = reader.nextLine().split(", ");

			for(String i : str_config) {
				config.add(Double.parseDouble(i));
			}

			reader.close();

		} catch (FileNotFoundException e) {
			System.err.println("Error: while reading config file");
			System.err.println(e);
		}

		return config;
	}

	public static int readFromAgentFile() {
        int agentNumber = 0;
        String inputPath = "src/test/java/agentnumber.txt";

        try {
			File agentFile = new File(inputPath);
			Scanner reader = new Scanner(agentFile);
			agentNumber = reader.nextInt();

			reader.close();

		} catch (FileNotFoundException e) {
			System.err.println("Error: while reading config file");
			System.err.println(e);
            System.exit(-1);
		}

        return agentNumber;
    }
	
	// Vector calculating helping functions
	static dPoint getVector(Point start, Point end) {
    	
		dPoint result = new dPoint(end.x-start.x, end.y-start.y);
    	
    	return result;
	}
	
	static double magnitudeD(dPoint a) {
		return Math.sqrt(Math.pow(a.x, 2) + Math.pow(a.y, 2));
	}
	
	static double magnitude(int x, int y) {
		return Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2));
	}

    static dPoint normalizeVector(dPoint a) {

    	double magnitude = magnitudeD(a);


    	dPoint result = new dPoint((double) a.x/magnitude, (double) a.y/magnitude);

    	return result;
    }

    static dPoint rotate(dPoint a, double angle) {

    	double qx = (Math.cos(angle) * (a.x)) - (Math.sin(angle) * (a.y));
    	double qy = (Math.sin(angle) * (a.x)) + (Math.cos(angle) * (a.y));

    	dPoint result = new dPoint(qx, qy);

    	return result;
    }

    static dPoint scale(dPoint vector,double magnitude) {
    	dPoint result = new dPoint(vector.x * magnitude, vector.y * magnitude);

    	return result;
    }
    
    static double angle_to_next_checkpoint(Point current, Point c1, Point c2) {
    	return Math.atan2(c2.y - c1.y, c2.x - c1.x) - Math.atan2(current.y - c1.y, current.x - c1.x);
    }
    
    static Point addVectors(Point first_checkpoint, dPoint b) {
    	Point result = new Point((int) Math.round(first_checkpoint.x + b.x), (int) Math.round(first_checkpoint.y + b.y));
    	return result;
    }
    
    static Point get_closest_point_on_vector_to_point(Point current, Point next_checkpoint, Point checkpoint_center) {
    	double x1 = (double) current.x, y1 = (double) current.y;
    	double x2 = (double) next_checkpoint.x, y2 = (double) next_checkpoint.y;
    	double x3 = (double) checkpoint_center.x, y3 = (double) checkpoint_center.y;
    	double dx = x2 - x1, dy = y2 - y1;
    	double det = dx * dx + dy * dy;
    	double a = (dy * (y3 - y1) + dx * (x3 - x1))/det;
    	return new Point((int) Math.round(x1 + a * dx), (int) Math.round(y1 + a * dy));
    }
    
    
    // Star function that controls the fundamental things
    static double sigmoid(double x, double L, double k, double xo) {
    	return L/(1 + Math.pow(Math.E, -k * (x - xo)));
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
        int agentNum = readFromAgentFile();
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
    	ArrayList<Double> config = readFromConfigFile("src/test/java/individuals_configurations/" + filename + ".txt");
        
        
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
            Point second_checkpoint = targets.get((target + 1) % targets.size());  // Target immediately after the intended

            Point current = new Point(x, y);

            // AGENT LOGIC
            

            // Parameters we control
            double focus_angle = config.get(0);  // Math.PI/2  Essentially the cone in which the checkpoint must be in wrt the velocity vector
            double corrective_thrust = config.get(1);  // 100  The fixed amount of thrust used when correcting the velocity vector
            
            // Offset related
            
            double scale_offset = config.get(2);  // 1   This must be adjusted depending on the value of the angles
            double step_constant_offset = config.get(3);  // 0.002   Steepness (or rate of change)
            double midpoint_val_offset = config.get(4); // 2000   Value of all_influences at which sigmoid result is half of max_offset
            double max_offset = config.get(5);  // 600   Maximum offset allowed
            
            // Thrust related
            double scale_thrust = config.get(6);  // 1   Scales all the influences accordingly
            double step_constant_thrust = config.get(7);  // 0.005   Steepness (or rate of change)
            double midpoint_val_thrust = config.get(8);  // 200   Value of all_influences at which sigmoid result is half of max_thrust
            double max_thrust = config.get(9);  // 200 This one we will leave at maximum because we prefer to change other variables first

            // -- LOGIC --
            
            // OPTIMAL POINT IN CHECKPOINT AREA
            
            // First, let's find the most efficient point to reach
            Point closest_point_current_to_second = get_closest_point_on_vector_to_point(current, second_checkpoint, first_checkpoint);
            dPoint checkpoint_to_closest = getVector(first_checkpoint, closest_point_current_to_second);
            double distance_to_closest_point = magnitudeD(checkpoint_to_closest);
            
            // Assuming that point is outside the checkpoint area, so we will use the point on the circumference that is closest
        	dPoint rim_point = scale(normalizeVector(checkpoint_to_closest), 300);
            Point new_first_checkpoint = new Point(first_checkpoint.x + (int) Math.round(rim_point.x), first_checkpoint.y + (int) Math.round(rim_point.y));
            if (distance_to_closest_point <= 300) {
            	// Point is within the checkpoint area, so we will aim for that
            	new_first_checkpoint = closest_point_current_to_second;
            }
            
            
            // OFFSET
            
            // Let's now determine the offset point to which we want to aim
            
            // First, we need a unit vector that is perpendicular to that of the vector current->first_checkpoint
            dPoint dir_current_first = getVector(current, new_first_checkpoint);
            dPoint normed = normalizeVector(dir_current_first);
            dPoint rotated = rotate(normed, Math.PI/2);  // pi radians (90 degrees) rotation "clockwise"
            
            // Then we need to consider everything that will influence how much this vector will be scaled
            
            // The closer the angle is to pi, the smaller the offset is, with 0 offset when perfectly aligned
            double angle_to_next_checkpoint = angle_to_next_checkpoint(current, new_first_checkpoint, second_checkpoint);
            double angle_influence = Math.abs(Math.PI - Math.abs(angle_to_next_checkpoint));  // The closer to pi, the smaller the offset
            if (angle_to_next_checkpoint <= 0) {
            	// Angle is greater than pi radians, which means ship must first go left before going right
            	// Therefore, we must flip the vector
            	rotated.x = -rotated.x;
            	rotated.y = -rotated.y;
            }
            
            // The further the checkpoint is, the greater the offset can be
            double distance_influence = new_first_checkpoint.distance(current);
            
            // We multiply all influences
            double all_influences = distance_influence * angle_influence * scale_offset;
            
            // We obtain the final scaling of the unit vector, contained in a finite range from 0 to 600
            double final_scaling = sigmoid(all_influences, max_offset, step_constant_offset, midpoint_val_offset);
            
            // We apply the scaling
            dPoint scaled = scale(rotated, final_scaling);
            
            // We obtain the offset point
            Point final_point = addVectors(new_first_checkpoint, scaled);
            
            
            // THRUST
            
            // Let's now determine how much thrust we must exert
            
            // If the next target is somewhat straight ahead, full thrust
            double thrust_angle_influence = Math.PI - angle_influence;  // The closer to pi, the higher the thrust (the reverse of angle_influence)
            
            // The greater the distance between the first checkpoint and the second one, the higher the thrust
            double distance_to_next_target = new_first_checkpoint.distance(second_checkpoint);
            
            // The faster we are going, the less thrust we need to add
            double speed = magnitude(vx, vy);
            double speed_influence = (1 / (1 + (speed/1000)));
            
            // We multiply all the influences
            double all_thrust_influences = thrust_angle_influence * distance_to_next_target * scale_thrust;
            
            // We obtain the final thrust, contained in a finite range from 0 to 200
            double thrust = sigmoid(all_thrust_influences, max_thrust, step_constant_thrust, midpoint_val_thrust) * speed_influence;
            
            
            // SPECIAL OVERRIDING CASES
            
            // If the target is the last one to reach, full thrust straight towards the target
            if (target == targets.size() - 1) {
            	final_point.x = first_checkpoint.x;
            	final_point.y = first_checkpoint.y;
            	thrust = 200;
            }
            
            
            // If the ship's current velocity vector is not going at least a little bit in the right direction, we correct it
            // by aiming the ship in the opposite direction with full thrust
            Point velocity = new Point(current.x + vx, current.y + vy);  // Velocity vector
            double angle_vel_off_course = Math.abs(angle_to_next_checkpoint(velocity, current, new_first_checkpoint));
            
            // If the velocity isn't in a "cone of vision" of 45º to each side of the line current->first_checkpoint, it must be corrected.
            if (angle_vel_off_course >= focus_angle/2 && speed > 40 && distance_influence > 400) {  // Below 40 speed is manageable
            	final_point.x = current.x - vx;
            	final_point.y = current.y - vy;
            	
            	// Just painting the target in the opposite direction could make the ship turn the wrong way. We need to add a little incentive
            	// in turning the way towards the objective
            	dPoint correction = getVector(final_point, new_first_checkpoint);
            	double correction_magnitude = magnitudeD(correction);
            	correction = scale(normalizeVector(correction), correction_magnitude/5);
            	
            	final_point.x = final_point.x + (int) Math.round(correction.x);
            	final_point.y = final_point.y + (int) Math.round(correction.y);
            	
            	thrust = corrective_thrust;
            }
            
//            System.out.println("Dir: " + dir_current_first.x + " " + dir_current_first.y);
//            System.out.println("Norm: " + normed.x + " " + normed.y);
//            System.out.println("Rotated: " + rotated.x + " " + rotated.y);
//            System.out.println("Angle to next checkpoint: " + angle_to_next_checkpoint);
//            System.out.println("Distance: " + distance_influence);
//            System.out.println("Final magnification: " + final_scaling);
//            System.out.println("Magnified: " + scaled.x + " " + scaled.y);
//            System.out.println("Velocity: " + vx + ", " + vy + " --> " + speed);
//            System.out.println("Thrust angle influence: " + thrust_angle_influence);
//            System.out.println("Final thrust: " + thrust);
//            System.out.println("Offset point result: " + offset_point.x + " " + offset_point.y);
            
            
            System.out.println(final_point.x + " " + final_point.y + " " + (int) thrust + " Agent " + agentNum); // X Y THRUST MESSAGE
            
        }
    }
}
