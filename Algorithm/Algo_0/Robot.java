﻿package mdp.g18.sim;

public class Robot {
	
	public static final int ROBOT_SIZE = 3;

	private int xCoordinate; // x coordinate
	private int yCoordinate; // y coordinate 
	private Direction direction;  // orientation
	
	Robot(int x, int y, Direction direction){
		this.xCoordinate = x;
		this.yCoordinate = y;
		this.direction = direction;
		
	}
	
	public int getxCoordinate() {
		return this.xCoordinate;
	}
	
	public void setxCoordinate(int x) {
		this.xCoordinate = x;
	}

	public int getyCoordinate() {
		return this.yCoordinate;
	}
	
	public void setyCoordinate(int y) {
		this.yCoordinate = y;
	}
	
	public char enumToChar(Direction dir) {
		
		char newString = switch (direction) {
		case NORTH -> 'N';
		case SOUTH -> 'S';
		case EAST -> 'E';
		case WEST -> 'W';
		default -> 'N';
		};

		return newString;
	}
	
	public Direction getDirection() {
		return this.direction;
	}
	
	public void setDirection(Direction dir) {
		this.direction = dir;
	}
	
	public void turnLeft(Direction direction){
		
		Direction dir = switch (direction) {
		case NORTH -> Direction.WEST;
		case SOUTH -> Direction.EAST;
		case EAST -> Direction.NORTH;
		case WEST -> Direction.SOUTH;
		default -> Direction.UNSET;
		};
		
		setDirection(dir);
	}
	
	public void turnRight(Direction direction){
		
		Direction dir = switch (direction) {
		case NORTH -> Direction.EAST;
		case SOUTH -> Direction.WEST;
		case EAST -> Direction.SOUTH;
		case WEST -> Direction.NORTH;
		default -> Direction.UNSET;
		};
		
		setDirection(dir);
	}
	
	public void forward(Direction direction){
		int x = this.getxCoordinate();
		int y = this.getyCoordinate();
		
		switch (direction) {
		case NORTH:
			y -= 1;
			break;
		case SOUTH:
			y += 1;
			break;
		case EAST:
			x += 1;
			break;
		case WEST:
			x -= 1;
			break;
		default:
			break;
		}
		
		this.setxCoordinate(x);
		this.setyCoordinate(y);
	}
	
	public void reverse(Direction direction){
		int x = this.getxCoordinate();
		int y = this.getyCoordinate();
		
		switch (direction) {
		case NORTH:
			y += 1;
			break;
		case SOUTH:
			y -= 1;
			break;
		case EAST:
			x -= 1;
			break;
		case WEST:
			x += 1;
			break;
		default:
			break;
		}
		
		this.setxCoordinate(x);
		this.setyCoordinate(y);
	}
}