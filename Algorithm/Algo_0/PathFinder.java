package mdp.g18.sim;

import java.awt.Color;
import java.awt.Graphics;
import java.util.ArrayList;
import java.util.Arrays;

public class PathFinder {
	
	private ArrayList<Data> pathCoordinates = new ArrayList<Data>();
	private ArrayList<Data> pathCoordinatesEnding = new ArrayList<Data>();
	private ArrayList<Obstacle> obstacleList = new ArrayList<Obstacle>();
	private ArrayList<Node> nodes;
	
	private int[] robotPosition;
	private int[] prevPosition;
	private char prevOrientation;
	private Direction reverseDir;
	private Data reverseData;
	
	private SimulatorRobot robot;
	private Obstacle obstacle;
	private Astar astar;
	
	private Node start;
	private Node target;
	private Node result;
	private String pathString;
	private String STMmovement;
	private ArrayList<Data> newData = new ArrayList<Data>();
	
	PathFinder(SimulatorRobot robot, ArrayList<Obstacle> obstacleList){
		this.robot = robot;
		this.setRobotPosition(new int[] {this.robot.getxCoordinate(), this.robot.getyCoordinate()}, Direction.UNSET);
		this.obstacleList = obstacleList;
		
		if (astar == null) {
			astar = new Astar(this.obstacleList,this.robot);
		}
	}
	
	public void getClosestObstacle() {
		if (getCurrentObstacle() == null) {
			Obstacle newObstacle = astar.getNextObstacle(null);
			if (newObstacle != null) {
				setObstacle(newObstacle);
			}
		}else {
			Obstacle prev = getCurrentObstacle();
			Obstacle newObstacle = astar.getNextObstacle(prev);
			if (newObstacle != null) {
				setObstacle(newObstacle);
			}
		}
	}
	
	public String findBestPath() {
		
		char originalDir = this.robot.enumToChar(this.robot.getDirection());
		this.STMmovement = "";
		
		this.nodes = astar.createAllNodes(); // create all nodes
		this.start = this.findNode(this.robotPosition);
		this.target = this.findNode(new int[] {this.obstacle.getxImageCoordinate(), -(Arena.GRIDNO - this.obstacle.getyImageCoordinate() - 1)});
		this.result = Astar.AstarSearch(this.start, this.target, originalDir);
		this.newData = astar.findPath(this.result); // in order
		if (this.newData != null) {
			this.pathCoordinates.addAll(this.newData);
			this.setRobotPosition(this.pathCoordinates.get(this.pathCoordinates.size() - 1).getCoordinates(), this.obstacle.getDirection());
			this.reverseData = new Data(this.robotPosition[0], this.robotPosition[1], this.reverseDir);
			this.newData.add(this.reverseData);
			this.pathCoordinates.add(this.reverseData);
			
			this.pathString = this.pathToString(originalDir,this.newData);
			this.STMmovement = this.combineStringSTM();
			this.prevPosition = this.pathCoordinates.get(this.pathCoordinates.size() - 1).getCoordinates();
			this.prevOrientation = this.pathCoordinates.get(this.pathCoordinates.size() - 1).getOrientation();
			
			return String.format("%s;%s", this.STMmovement , this.pathString); 
		} else {
			return "CannotFind";
		}
	}
	
	/*private String combineStringSTM() {
		String combineString = "";
		ArrayList<String> stringOfCommands = new ArrayList<String>(Arrays.asList(this.STMmovement.split(",")));
		String[] stringArray = new String[stringOfCommands.size()];
		int i = 0;
		String newString = "STMI,";
		
		for (String s: stringOfCommands) {
			stringArray[i] = s;
			i++;
		}
		
		String nextString = "";
		String nextNextString = "";
		String prevString = "";
		i = 0;
		
		while (i < stringArray.length) {
			
			if(i < stringArray.length - 2) { // not second last
				nextString = stringArray[i + 1];
				nextNextString = stringArray[i + 2];
				
				if (stringArray[i].contains("f") && (nextString.contains("l") || nextString.contains("r")) && nextNextString.contains("f")) {
					
					if (!combineString.isEmpty()) {
						newString += String.format("%s,",combineString);
						combineString = "";
					}
					
					if (nextString.contains("l")) {
						newString += "a088,";
					}
					else if (nextString.contains("r")) {
						newString += "d090,";
					}
					i += 3;
				} 
				else if(stringArray[i].compareTo(nextString) == 0) {
					
					if (combineString.isEmpty()) {
						combineString = stringArray[i];
					}
					else
						combineString = combineString.substring(0, 1) + String.format("%03d",(Integer.parseInt(combineString.substring(1, 4)) + Integer.parseInt(stringArray[i].substring(1, 4))));
					i++;
				}
				else {
					if (!combineString.isEmpty()) {
						if(i != 0) {
							prevString = stringArray[i - 1];
							//System.out.println(String.format("%d,%s", i,combineString));
							if(stringArray[i].compareTo(prevString) == 0) {
								combineString = combineString.substring(0, 1) + String.format("%03d",(Integer.parseInt(combineString.substring(1, 4)) + Integer.parseInt(stringArray[i].substring(1, 4))));
							}
						}
						newString += String.format("%s,",combineString);
						combineString = "";
					}
					else 
						newString += String.format("%s,",stringArray[i]);
					i++;
				}
			}
			
			// if second last and last
			if (i >= stringArray.length - 2) {
				if (i ==  stringArray.length - 2) {
					if (!combineString.isEmpty() && stringArray[i].contains("f")) {
						combineString = combineString.substring(0, 1) + String.format("%03d",(Integer.parseInt(combineString.substring(1, 4)) + Integer.parseInt(stringArray[i].substring(1, 4))));
						newString += String.format("%s,",combineString);
						combineString = "";
					}
					else {
						newString += String.format("%s,",stringArray[i]);
					}
					i++;
				}
				newString += String.format("%s",stringArray[i]);
				break;
			}
		}
		
		return newString;
	}*/
	
	private String combineStringSTM() {
		String newString = "STMI,";
		String combineString = "";
		ArrayList<String> stringOfCommands = new ArrayList<String>(Arrays.asList(this.STMmovement.split(",")));
		String stringArray[] = new String[stringOfCommands.size()];
		int i = 0;
 		
		String nextString = "";
		String prevString = "";
		
		for (String s: stringOfCommands) {
			stringArray[i] = s;
			i++;
		}
		
		
		for (i = 0; i < stringOfCommands.size(); i++) {
			if(i != stringOfCommands.size() - 1) {
				
				nextString = stringArray[i + 1];
				if(nextString.compareTo(stringArray[i]) == 0) {
					if (combineString.isEmpty()) {
						combineString = stringArray[i];
					}
					else
						combineString = combineString.substring(0, 1) + String.format("%03d",(Integer.parseInt(combineString.substring(1, 4)) + Integer.parseInt(stringArray[i].substring(1, 4))));
				}
				else {
					if (!combineString.isEmpty()) {
						if(i != 0) {
							prevString = stringArray[i - 1];
							//System.out.println(String.format("%d,%s", i,combineString));
							if(prevString.compareTo(stringArray[i]) == 0) {
								combineString = combineString.substring(0, 1) + String.format("%03d",(Integer.parseInt(combineString.substring(1, 4)) + Integer.parseInt(stringArray[i].substring(1, 4))));
							}
						}
						newString += String.format("%s,",combineString);
						combineString = "";
					}
					else 
						newString += String.format("%s,",stringArray[i]);
				}
			}
			
			// if last
			if (i == stringOfCommands.size() - 1) {
				if (!combineString.isEmpty()) 
					newString += String.format("%s,",combineString);
				newString += String.format("%s",stringArray[i]);
			}
		}
		
		return newString;
	}
	
	/*private String pathToString(char originalDir, ArrayList <Data> dataPoints) {
		Direction currentDir = this.robot.getDirection();
		int[] xCoordinate = new int[dataPoints.size()]; 
		int[] yCoordinate = new int[dataPoints.size()]; 
		char[] directionArray = new char[dataPoints.size()];
		char currentMovement ='\0';
		int i = 0;
		
		char nextMovement;
		char nextNextMovement;
		int[] nextNextCoord = new int[2];
		String prevString = "";
		String android = "ANDROID|";
		
		
		for (Data d : dataPoints) {
			
			if(dataPoints.indexOf(d) != dataPoints.size() - 1) { //while not last
				currentDir = this.movement(currentDir, new int[] {dataPoints.get(dataPoints.indexOf(d) + 1).getElement(0),dataPoints.get(dataPoints.indexOf(d) + 1).getElement(1)});
				d.setOrientation(currentDir);
			}
			
			xCoordinate[i] = d.getElement(0);
			yCoordinate[i] = d.getElement(1);
			directionArray[i] = d.getOrientation(); 
			i++;
		}
		
		i = 0;
		
		if(this.prevPosition == null && dataPoints.get(0).getOrientation() != originalDir) {
			android += String.format("ROBOT,%d,%d,%c:", dataPoints.get(0).getElement(0), -dataPoints.get(0).getElement(1), dataPoints.get(0).getOrientation());
		}
		
		if (this.prevPosition != null) {
			android += String.format("ROBOT,%d,%d,%c:", this.prevPosition[0], -this.prevPosition[1], dataPoints.get(0).getOrientation());
		}
				
		
		while (i < xCoordinate.length) {
			
			if(i < xCoordinate.length - 2) {
				currentMovement = directionArray[i];
				nextMovement = directionArray[i + 1];
				nextNextMovement = directionArray[i + 2];
				
				if (currentMovement != nextMovement) {
					
					// get coord of i + 2
					nextNextCoord = new int[] {xCoordinate[i + 2],yCoordinate[i + 2]};
					
					//if diagonal
					if(Math.abs(nextNextCoord[0] - xCoordinate[i]) == 1 && Math.abs(nextNextCoord[1] - yCoordinate[i]) == 1) {
						if (i != 0 && prevString.compareTo(String.format("ROBOT,%d,%d,%c:", xCoordinate[i], - yCoordinate[i], directionArray[i])) != 0)
							android += String.format("ROBOT,%d,%d,%c:", xCoordinate[i], - yCoordinate[i], directionArray[i]);
						
						if (currentMovement == nextNextMovement) {
							android += String.format("ROBOT,%d,%d,%c:", xCoordinate[i + 2], - yCoordinate[i + 2], directionArray[i +1]);
						}
						
						android += String.format("ROBOT,%d,%d,%c:", xCoordinate[i + 2], - yCoordinate[i + 2], directionArray[i + 2]);
						prevString = String.format("ROBOT,%d,%d,%c:", xCoordinate[i + 2], - yCoordinate[i + 2], directionArray[i + 2]);
						i += 2;
					} else{
						android += String.format("ROBOT,%d,%d,%c:", xCoordinate[i + 1], - yCoordinate[i + 1], directionArray[i]);
						android += String.format("ROBOT,%d,%d,%c:", xCoordinate[i + 1], - yCoordinate[i + 1], directionArray[i + 1]);
						prevString = String.format("ROBOT,%d,%d,%c:", xCoordinate[i + 1], - yCoordinate[i + 1], directionArray[i + 1]);
						i ++;
					}
				} else {
					i++;
				}
			}
				
			if (i >= xCoordinate.length - 2) {
				if (i ==  xCoordinate.length - 2 && prevString.compareTo(String.format("ROBOT,%d,%d,%c:", xCoordinate[i], - yCoordinate[i], directionArray[i])) != 0) {
					android += String.format("ROBOT,%d,%d,%c:", xCoordinate[i], - yCoordinate[i], directionArray[i]);
				}
				i++;
				android += String.format("ROBOT,%d,%d,%c", xCoordinate[i], - yCoordinate[i], directionArray[i]);
				break;
			}	
		}

		return android;
	}*/
	
	private String pathToString(char originalDir, ArrayList <Data> dataPoints) {
		Direction currentDir = this.robot.getDirection();
		char currentMovement ='\0';
		char nextMovement; 
		
		String andriod = "ANDROID|";
		
		for (Data d: dataPoints) {
			
			if(dataPoints.indexOf(d) != dataPoints.size() - 1) { //while not last
				currentDir = this.movement(currentDir, new int[] {dataPoints.get(dataPoints.indexOf(d) + 1).getElement(0),dataPoints.get(dataPoints.indexOf(d) + 1).getElement(1)});
				d.setOrientation(currentDir);
			}
		}
		
		if(this.prevPosition == null && dataPoints.get(0).getOrientation() != originalDir) {
			andriod += String.format("ROBOT,%d,%d,%c:", dataPoints.get(0).getElement(0), -dataPoints.get(0).getElement(1), dataPoints.get(0).getOrientation());
		}
		
		if (this.prevPosition != null) {
			andriod += String.format("ROBOT,%d,%d,%c:", this.prevPosition[0], -this.prevPosition[1], dataPoints.get(0).getOrientation());
		}
		
		for (Data d: dataPoints) {
			currentMovement = d.getOrientation();
			
			if(dataPoints.indexOf(d) != dataPoints.size() - 1) {
				nextMovement = dataPoints.get(dataPoints.indexOf(d) + 1).getOrientation();
				
				if (currentMovement != nextMovement) {
					andriod += String.format("ROBOT,%d,%d,%c:", dataPoints.get(dataPoints.indexOf(d) + 1).getElement(0), -dataPoints.get(dataPoints.indexOf(d) + 1).getElement(1), d.getOrientation());
					andriod += String.format("ROBOT,%d,%d,%c:", dataPoints.get(dataPoints.indexOf(d) + 1).getElement(0), -dataPoints.get(dataPoints.indexOf(d) + 1).getElement(1), dataPoints.get(dataPoints.indexOf(d) + 1).getOrientation());
				}
			}
			
			if (dataPoints.indexOf(d) == dataPoints.size() - 1) {
				andriod += String.format("ROBOT,%d,%d,%c:", dataPoints.get(dataPoints.indexOf(d) - 1).getElement(0), -dataPoints.get(dataPoints.indexOf(d) - 1).getElement(1), dataPoints.get(dataPoints.indexOf(d) - 1).getOrientation());
				andriod += String.format("ROBOT,%d,%d,%c", d.getElement(0), -d.getElement(1), d.getOrientation());
			}
			
		}
		
		return andriod;
		
		}
		
	private Direction movement(Direction currentDir, int[] point) {
		
		switch(currentDir) {
		
		case NORTH:
			if (point[0] == this.robot.getxCoordinate() && point[1] < this.robot.getyCoordinate()) {
				this.robot.forward(currentDir);
				this.STMmovement += "f010,";
			} else if (point[0] == this.robot.getxCoordinate() && point[1] > this.robot.getyCoordinate()) {
				this.robot.reverse(currentDir);
				this.STMmovement += "b010,";
			} else if (point[0] > this.robot.getxCoordinate() && point[1] == this.robot.getyCoordinate()) {
				this.robot.turnRight(currentDir);
				this.robot.forward(this.robot.getDirection());
				this.STMmovement += "r090,f010,";
			} else if (point[0] < this.robot.getxCoordinate() && point[1] == this.robot.getyCoordinate()) {
				this.robot.turnLeft(currentDir);
				this.robot.forward(this.robot.getDirection());
				this.STMmovement += "l090,f010,";
			}
			break;
			
		case SOUTH:
			if (point[0] == this.robot.getxCoordinate() && point[1] < this.robot.getyCoordinate()) {
				this.robot.reverse(currentDir);
				this.STMmovement += "b010,";
			} else if (point[0] == this.robot.getxCoordinate() && point[1] > this.robot.getyCoordinate()) {
				this.robot.forward(currentDir);
				this.STMmovement += "f010,";
			} else if (point[0] < this.robot.getxCoordinate() && point[1] == this.robot.getyCoordinate()) {
				this.robot.turnRight(currentDir);
				this.robot.forward(this.robot.getDirection());
				this.STMmovement += "r090,f010,";
			} else if (point[0] > this.robot.getxCoordinate() && point[1] == this.robot.getyCoordinate()) {
				this.robot.turnLeft(currentDir);
				this.robot.forward(this.robot.getDirection());
				this.STMmovement += "l090,f010,";
			}
			break;
			
		case EAST:
			if (point[0] == this.robot.getxCoordinate() && point[1] < this.robot.getyCoordinate()) {
				this.robot.turnLeft(currentDir);
				this.robot.forward(this.robot.getDirection());
				this.STMmovement += "l090,f010,";
			} else if (point[0] == this.robot.getxCoordinate() && point[1] > this.robot.getyCoordinate()) {
				this.robot.turnRight(currentDir);
				this.robot.forward(this.robot.getDirection());
				this.STMmovement += "r090,f010,";
			} else if (point[0] < this.robot.getxCoordinate() && point[1] == this.robot.getyCoordinate()) {
				this.robot.reverse(currentDir);
				this.STMmovement += "b010,";
			} else if (point[0] > this.robot.getxCoordinate() && point[1] == this.robot.getyCoordinate()) {
				this.robot.forward(currentDir);
				this.STMmovement += "f010,";
			}
			break;
			
		case WEST:
			if (point[0] == this.robot.getxCoordinate() && point[1] < this.robot.getyCoordinate()) {
				this.robot.turnRight(currentDir);
				this.robot.forward(this.robot.getDirection());
				this.STMmovement += "r090,f010,";
			} else if (point[0] == this.robot.getxCoordinate() && point[1] > this.robot.getyCoordinate()) {
				this.robot.turnLeft(currentDir);
				this.robot.forward(this.robot.getDirection());
				this.STMmovement += "l090,f010,";
			} else if (point[0] < this.robot.getxCoordinate() && point[1] == this.robot.getyCoordinate()) {
				this.robot.forward(currentDir);
				this.STMmovement += "f010,";
			} else if (point[0] > this.robot.getxCoordinate() && point[1] == this.robot.getyCoordinate()) {
				this.robot.reverse(currentDir);
				this.STMmovement += "b010,";
			}
			break;
		default:
			break;
		}
		
		return this.robot.getDirection();
	}
	
	public void setRobotPosition(int[] robotPos, Direction dir) {
		
		this.robotPosition = robotPos;
		
		int x = this.robotPosition[0];
		int y = this.robotPosition[1];
		
		switch (dir) { // obstacle direction
		case NORTH:
			y -= 1;
			this.reverseDir = Direction.SOUTH;
			break;
		case SOUTH:
			y += 1;
			this.reverseDir = Direction.NORTH;
			break;
		case EAST:
			x += 1;
			this.reverseDir = Direction.WEST;
			break;
		case WEST:
			x -= 1;
			this.reverseDir = Direction.EAST;
			break;
		default:
			break;
		}
		
		this.robotPosition = new int[] {x,y};
	}
	
	public void setRobot(SimulatorRobot robot) {
		this.robot = robot;
	}
	
	public SimulatorRobot getRobot() {
		return this.robot;
	}
	
	public void setObstacle(Obstacle obstacle) {
		this.obstacle = obstacle;
	}
	
	public Obstacle getCurrentObstacle() {
		return this.obstacle;
	}
	
	public ArrayList<Data> getpathCoordinates(){
		return this.pathCoordinates;
	}
	
	public ArrayList<Data> getpathCoordinatesEnd(){
		return this.pathCoordinatesEnding;
	}
	
	public int[] getPrevPosition() {
		return this.prevPosition;
	}
	
	public char getPrevOrientation() {
		return this.prevOrientation;
	}
	
	public void paintPath(Graphics g) {
		g.setColor(Color.white);
		for(Data path: getpathCoordinates()) {
			g.fillRect((path.getElement(0)) * Arena.UNIT_SIZE, (Arena.GRIDNO + path.getElement(1) - 1) * Arena.UNIT_SIZE + Arena.UNIT_SIZE, Arena.UNIT_SIZE, Arena.UNIT_SIZE);
		}
	}
	
	private Node findNode(int[] coord) {
		
		for (Node node : this.nodes) {
			if(node.getCoord()[0] == coord[0] && node.getCoord()[1] == coord[1]) {
				return node;
			}
		}
		
		return null;
	}
}