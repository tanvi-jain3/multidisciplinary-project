package mdp.g18.sim;

import java.awt.Color;
import java.awt.Graphics;

public class Obstacle {

	private int obstacleID;
	// coordinates at bottom right-hand side
	private int xCoordinate; // x coordinate
	private int yCoordinate; // y coordinate 
	private int xImageCoordinate; // x coordinate
	private int yImageCoordinate; // y coordinate 
	private Direction direction;  // orientation

	private static final int LENGTH = 1;
	
	
	Obstacle(int id,int xCoordinate,int yCoordinate, Direction direction){
		this.obstacleID = id;
		this.xCoordinate = xCoordinate;
		this.yCoordinate = yCoordinate;
		this.direction = direction;
		setImageCoord(direction);
	}
	
	public void setObstacleID(int id) {
		this.obstacleID = id;
	}
	
	public int getObstacleID() {
		return this.obstacleID;
	}
	
	public int getxCoordinate() {
		return this.xCoordinate;
	}

	public int getyCoordinate() {
		return this.yCoordinate;
	}
	
	public int getxImageCoordinate() {
		return this.xImageCoordinate;
	}

	public int getyImageCoordinate() {
		return this.yImageCoordinate;
	}

	private void setDirection(Direction dir) {
		this.direction = dir;
	}
	
	public Direction getDirection() {
		return this.direction;
	}
	
	public void setImageCoord(Direction dir) {
		
		switch(dir) {
		case NORTH:
			this.xImageCoordinate = this.getxCoordinate();
			this.yImageCoordinate = this.getyCoordinate() - 3;
			break;
		case EAST:
			this.xImageCoordinate = this.getxCoordinate() + 3;
			this.yImageCoordinate = this.getyCoordinate();
			break;
		case WEST:
			this.xImageCoordinate = this.getxCoordinate() - 3;
			this.yImageCoordinate = this.getyCoordinate();
			break;
		case SOUTH:
			this.xImageCoordinate = this.getxCoordinate();
			this.yImageCoordinate = this.getyCoordinate() + 3;
			break;
		default:
			break;
		}
	}

	public int getLength() { return LENGTH; }
	
	public void paintObstacle(Graphics g, boolean selector) {
		
		// Obstacle body
		if (selector) {
			g.setColor(Color.lightGray);
		}
		else {
			g.setColor(Color.blue);
		}
		
		g.fillRect(xCoordinate * Arena.UNIT_SIZE, yCoordinate * Arena.UNIT_SIZE + Arena.UNIT_SIZE, Arena.UNIT_SIZE, Arena.UNIT_SIZE);
		
	}
	
	// Set image direction of an obstacle
	public void selectImage(Graphics g, boolean selector, Direction dir) {
		if (selector) {
			g.setColor(Color.pink);
		}
		else {
			setImage(g, dir);
		}

		switch (dir) {
			case NORTH:
				// Color upper row of pixels
				g.fillRect(xCoordinate * Arena.UNIT_SIZE, yCoordinate * Arena.UNIT_SIZE, Arena.UNIT_SIZE, Arena.UNIT_SIZE);
				g.fillRect(xCoordinate * Arena.UNIT_SIZE, yCoordinate * Arena.UNIT_SIZE - Arena.UNIT_SIZE, Arena.UNIT_SIZE, Arena.UNIT_SIZE);
				g.fillRect(xCoordinate * Arena.UNIT_SIZE, yCoordinate * Arena.UNIT_SIZE - 2 * Arena.UNIT_SIZE, Arena.UNIT_SIZE, Arena.UNIT_SIZE);
				break;
				
			case SOUTH:
				g.fillRect(xCoordinate * Arena.UNIT_SIZE, yCoordinate * Arena.UNIT_SIZE + 2 * Arena.UNIT_SIZE, Arena.UNIT_SIZE, Arena.UNIT_SIZE);
				g.fillRect(xCoordinate * Arena.UNIT_SIZE, yCoordinate * Arena.UNIT_SIZE + 3 * Arena.UNIT_SIZE, Arena.UNIT_SIZE, Arena.UNIT_SIZE);
				g.fillRect(xCoordinate * Arena.UNIT_SIZE, yCoordinate * Arena.UNIT_SIZE + 4 * Arena.UNIT_SIZE, Arena.UNIT_SIZE, Arena.UNIT_SIZE);
				break;
				
			case EAST:
				g.fillRect(xCoordinate * Arena.UNIT_SIZE + Arena.UNIT_SIZE, yCoordinate * Arena.UNIT_SIZE + Arena.UNIT_SIZE, Arena.UNIT_SIZE, Arena.UNIT_SIZE);
				g.fillRect(xCoordinate * Arena.UNIT_SIZE + 2 * Arena.UNIT_SIZE, yCoordinate * Arena.UNIT_SIZE + Arena.UNIT_SIZE, Arena.UNIT_SIZE, Arena.UNIT_SIZE);
				g.fillRect(xCoordinate * Arena.UNIT_SIZE + 3 * Arena.UNIT_SIZE, yCoordinate * Arena.UNIT_SIZE + Arena.UNIT_SIZE, Arena.UNIT_SIZE, Arena.UNIT_SIZE);
				break;
				
			case WEST:
				g.fillRect(xCoordinate * Arena.UNIT_SIZE - Arena.UNIT_SIZE, yCoordinate * Arena.UNIT_SIZE + Arena.UNIT_SIZE, Arena.UNIT_SIZE, Arena.UNIT_SIZE);
				g.fillRect(xCoordinate * Arena.UNIT_SIZE - 2 * Arena.UNIT_SIZE, yCoordinate * Arena.UNIT_SIZE + Arena.UNIT_SIZE, Arena.UNIT_SIZE, Arena.UNIT_SIZE);
				g.fillRect(xCoordinate * Arena.UNIT_SIZE - 3 * Arena.UNIT_SIZE, yCoordinate * Arena.UNIT_SIZE + Arena.UNIT_SIZE, Arena.UNIT_SIZE, Arena.UNIT_SIZE);
				break;
				
			case UNSET:
				break;
		}
	}
	
	// Set image given coordinates
	public void setImage(Graphics g, Direction dir) {
		g.setColor(Color.magenta);
		setDirection(dir);
	}
}