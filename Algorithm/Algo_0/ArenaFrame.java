package mdp.g18.sim;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import javax.swing.JPanel;
import javax.swing.Timer;

import java.awt.event.*;
import java.awt.geom.Point2D;
import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.TimeUnit;

public class ArenaFrame extends JPanel implements ActionListener {
	
	public static int [][] obstacles = new int[Arena.GRIDNO][Arena.GRIDNO];
	private ArrayList<Obstacle> obstacleObjects = new ArrayList<Obstacle>();
	private ArrayList<Obstacle> obstacleCompleted = new ArrayList<Obstacle>();
	
	private String stringOfObstacles = "";
	
	private String newPathString = "";
	private int prevID = -1;
	private ArrayList<String> splitPathCoord;
	private ArrayList<String> listOfPaths = new ArrayList<String>();
	private ArrayList<String> listOfCoords= new ArrayList<String>();
	private ArrayList<String> combineString = new ArrayList<String>();
	
	public boolean loadObstacles = false;
	public boolean connectToRpi = false;
	public boolean findPath = false;
	
	public int mx = -100;
	public int my = -100;
	
	private Move move;
	private Click click;
	
	private Arena arena;
	private RPiClient client;
	private RealRobot robot;
	private SimulatorRobot simRobot;
	private PathFinder pathfinder;
	private Timer timer;
	
	ArenaFrame(){
		
		arena = new Arena();
		client = new RPiClient();
		robot = new RealRobot(1,-1, Direction.NORTH);
		
		move = new Move();
		this.addMouseMotionListener(move);
		
		click = new Click();
		this.addMouseListener(click);
		
		this.setPreferredSize(new Dimension(Arena.ARENA_WIDTH,Arena.ARENA_HEIGHT));
		
		// Initialize no obstacles
		for(int i = 0; i < Arena.GRIDNO; i++) {
			for(int j = 0; j < Arena.GRIDNO; j++) {
				obstacles[i][j] = -1;
			}
		}
	}
	
	public void paintComponent(Graphics g) {
		super.paintComponent(g);
		
		this.arena.paintArena(g);
		this.robot.drawRobot(g);
		
		if(this.loadObstacles) {
			for( Obstacle obstacle: obstacleObjects) {
				obstacle.paintObstacle(g, false);
				obstacle.selectImage(g, false, obstacle.getDirection());
			}
		}
		
		if (pathfinder != null) {
			pathfinder.paintPath(g);
		}
		
		// Simulation
		if(findPath) {
			timer = new Timer(500,this);
			timer.start();
		}
		
	}
	
	public void connectToRPI() {
		
		try {
			client.startConnection();
			System.out.println("RPi connected.");
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		this.waitForRPIMessage();
	}
	
	// Wait for RPI to send message
	public void waitForRPIMessage() {
		this.connectToRpi = true;
		String newString = "";
		while(this.connectToRpi) {
				//System.out.println(client.receiveMsg());
			newString = client.receiveMsg();
			System.out.println(newString);
			if (!newString.isEmpty()) {
				if(newString.compareTo("g") != 0) {
					this.stringOfObstacles = newString;
					System.out.println(this.stringOfObstacles);
				}
				this.connectToRpi = false;
			}
		}
	}
		
		public void sendRPIMessage() {
			
			String newString = "";
			String recvString = "";
			
			for(int i = 0;i < this.combineString.size();i++) {
				System.out.println(i);
				
				if (i == 0) {
					recvString = client.receiveMsg();
					System.out.println(recvString);
				}
					
				
				if(recvString.compareTo("StartDetection") == 0) {
					this.client.sendMsg(this.combineString.get(i));
					System.out.println(this.combineString.get(i));
					newString = client.receiveMsg();
					System.out.println(newString);
					if (!newString.isEmpty()) {
						if(newString.compareTo("g") == 0) {
							continue;
						}
					}
				}
			}
		}
	
	public class Move implements MouseMotionListener{
		@Override
		public void mouseDragged(MouseEvent e) {
			// TODO Auto-generated method stub
		}

		@Override
		public void mouseMoved(MouseEvent e) {
			mx = e.getX();
			my = e.getY();
			LabelFrame.xLabel.setText("X Coordinate : " + String.valueOf(coordinateX()));
			LabelFrame.yLabel.setText("Y Coordinate : " + String.valueOf(Arena.GRIDNO - coordinateY() - 1));
		}
	}
	
	public class Click implements MouseListener{

		@Override
		public void mouseClicked(MouseEvent e) {
			
		}

		@Override
		public void mousePressed(MouseEvent e) {
			// TODO Auto-generated method stub
			
		}

		@Override
		public void mouseReleased(MouseEvent e) {
		}

		@Override
		public void mouseEntered(MouseEvent e) {
			// TODO Auto-generated method stub
			
		}

		@Override
		public void mouseExited(MouseEvent e) {
			// TODO Auto-generated method stub
			
		}
	}
	
	@Override
	public void actionPerformed(ActionEvent e) {
		if (findPath) {
			findBestPath();
		}
		repaint();
	}
	
	public void drawObstacles(){
		// add obstacles from RPI message
		ArrayList<Object[]> msg = client.processString(this.stringOfObstacles);
		
		for (Object[] o : msg) {
			Obstacle obstacle = new Obstacle((Integer) o[0], (Integer)o[1], (Integer)o[2], (Direction) o[3]);
			addObstacle(obstacle);
			obstacleObjects.add(obstacle);
		}
		
		if(obstacleObjects.size() == obstacleObjects.size()) {
			this.loadObstacles = false;
		}
		
		repaint();
	}
	
	public void findBestPath() {
		
		if (this.pathfinder == null) {
			// create simulator robot --> no visualization
			this.simRobot = new SimulatorRobot(this.robot.getxCoordinate(),this.robot.getyCoordinate(),this.robot.getDirection());
			this.pathfinder = new PathFinder(this.simRobot, this.obstacleObjects);
		}
		
		if (this.pathfinder.getCurrentObstacle() == null) {
			this.pathfinder.getClosestObstacle();
		}
		
		if(this.simRobot != null && this.pathfinder.getCurrentObstacle() != null) {
			this.newPathString = this.pathfinder.findBestPath();
			
			if (this.newPathString.compareTo("CannotFind") == 0) {
				this.listOfPaths.add(String.format("STMI,f000,obs,%d",this.prevID));
				this.listOfCoords.add(String.format("ANDROID|ROBOT,%d,%d,%c", this.pathfinder.getPrevPosition()[0], -this.pathfinder.getPrevPosition()[1], this.pathfinder.getPrevOrientation()));
				for (int i = 0; i < this.listOfPaths.size(); i++) {
					//System.out.println(this.listOfPaths.get(i));
					//System.out.println(this.listOfCoords.get(i));
					this.combineString.add(String.format("%s|%s", this.listOfPaths.get(i),this.listOfCoords.get(i)));
				}
				this.sendRPIMessage();
				this.findPath = false;
				return;
			}

			this.splitPathCoord = new ArrayList<String>(Arrays.asList(this.newPathString.split(";")));
			
			this.listOfPaths.add(this.splitPathCoord.get(0));
			this.listOfCoords.add(this.splitPathCoord.get(1));
			
			/*for (int i = 0; i < this.listOfPaths.size(); i++) {
				System.out.println(this.listOfPaths.get(i));
				System.out.println(this.listOfCoords.get(i));
			}*/

			if (this.prevID != -1) {
				//System.out.println(this.listOfPaths.get(this.listOfPaths.size() - 1));
				String newString = String.format("%s,obs,%d",this.listOfPaths.get(this.listOfPaths.size() - 1),this.prevID);
				this.listOfPaths.remove(this.listOfPaths.size() - 1);
				this.listOfPaths.add(newString);
			}
			
			this.obstacleCompleted.add(this.pathfinder.getCurrentObstacle()); // add to obstacle completed in simulator
			this.prevID = this.pathfinder.getCurrentObstacle().getObstacleID();
			
			if(this.listOfPaths.size() >= this.obstacleObjects.size()) {
				this.listOfPaths.add(String.format("STMI,f000,obs,%d",this.prevID));
				this.listOfCoords.add(String.format("ANDROID|ROBOT,%d,%d,%c", this.pathfinder.getPrevPosition()[0], -this.pathfinder.getPrevPosition()[1], this.pathfinder.getPrevOrientation()));
			}
			
			if (this.obstacleCompleted.size() == this.obstacleObjects.size()) {
				this.findPath = false;
				
				for (int i = 0; i < this.listOfPaths.size(); i++) {
					//System.out.println(this.listOfPaths.get(i));
					//System.out.println(this.listOfCoords.get(i));
					this.combineString.add(String.format("%s|%s", this.listOfPaths.get(i),this.listOfCoords.get(i)));
				}
				
				for (String s: this.combineString) {
					System.out.println(s);
				}
				
				//this.sendRPIMessage();
				
			}
			else {
				this.pathfinder.getClosestObstacle();

			}
		}
	}
	
	public void addObstacle(Obstacle obstacle) {
		
		switch(obstacle.getDirection()) {
		case NORTH:
			for (int i = -1; i < 2; i++ ) {
				for (int j = -3; j < 2; j++ ) {
					if((obstacle.getxCoordinate() + i != obstacle.getxImageCoordinate() || obstacle.getyCoordinate() + j != obstacle.getyImageCoordinate()) &&
							obstacle.getxCoordinate() + i >= 0 && obstacle.getxCoordinate() + i < 20 && obstacle.getyCoordinate() + j >= 0 && obstacle.getyCoordinate() + j < 20)
						obstacles[obstacle.getxCoordinate() + i][obstacle.getyCoordinate() + j] = obstacle.getObstacleID();
				}
			}
			break;
		case SOUTH:
			for (int i = -1; i < 2; i++ ) {
				for (int j = -1; j < 4; j++ ) {
					if((obstacle.getxCoordinate() + i != obstacle.getxImageCoordinate() || obstacle.getyCoordinate() + j != obstacle.getyImageCoordinate()) &&
							obstacle.getxCoordinate() + i >= 0 && obstacle.getxCoordinate() + i < 20 && obstacle.getyCoordinate() + j >= 0 && obstacle.getyCoordinate() + j < 20)
						obstacles[obstacle.getxCoordinate() + i][obstacle.getyCoordinate() + j] = obstacle.getObstacleID();
				}
			}
			break;
		case EAST:
			for (int i = -1; i < 4; i++ ) {
				for (int j = -1; j < 2; j++ ) {
					if((obstacle.getxCoordinate() + i != obstacle.getxImageCoordinate() || obstacle.getyCoordinate() + j != obstacle.getyImageCoordinate()) &&
							obstacle.getxCoordinate() + i >= 0 && obstacle.getxCoordinate() + i < 20 && obstacle.getyCoordinate() + j >= 0 && obstacle.getyCoordinate() + j < 20)
						obstacles[obstacle.getxCoordinate() + i][obstacle.getyCoordinate() + j] = obstacle.getObstacleID();
				}
			}
			break;
		case WEST:
			for (int i = -3; i < 2; i++ ) {
				for (int j = -1; j < 2; j++ ) {
					if((obstacle.getxCoordinate() + i != obstacle.getxImageCoordinate() || obstacle.getyCoordinate() + j != obstacle.getyImageCoordinate()) &&
							obstacle.getxCoordinate() + i >= 0 && obstacle.getxCoordinate() + i < 20 && obstacle.getyCoordinate() + j >= 0 && obstacle.getyCoordinate() + j < 20)
						obstacles[obstacle.getxCoordinate() + i][obstacle.getyCoordinate() + j] = obstacle.getObstacleID();
				}
			}
			break;
		default:
			break;
		}
	}
	
	public int coordinateX() {
		for(int i = 0; i < Arena.GRIDNO; i++) {
			for(int j = 0; j < Arena.GRIDNO; j++) {
				if ((mx >= i * Arena.UNIT_SIZE) && (mx < i * Arena.UNIT_SIZE + Arena.UNIT_SIZE) && (my >= j * Arena.UNIT_SIZE + Arena.UNIT_SIZE) && (my < j * Arena.UNIT_SIZE + Arena.UNIT_SIZE + Arena.UNIT_SIZE)) {
					return i;
				}
			}
		}
		return -1;
	}
	
	// Find y-coordinate of mouse
	public int coordinateY() {
		for(int i = 0; i < Arena.GRIDNO; i++) {
			for(int j = 0; j < Arena.GRIDNO; j++) {
				if ((mx >= i * Arena.UNIT_SIZE) && (mx < i * Arena.UNIT_SIZE + Arena.UNIT_SIZE) && (my >= j * Arena.UNIT_SIZE + Arena.UNIT_SIZE) && (my < j * Arena.UNIT_SIZE + Arena.UNIT_SIZE + Arena.UNIT_SIZE)) {
					return j;
				}
			}
		}
		return -1;
	}
}