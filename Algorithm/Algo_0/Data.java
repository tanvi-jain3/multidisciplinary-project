﻿package mdp.g18.sim;

public class Data{
    private int[] data;
    private char orientation;

    public Data(int s1, int s2, Direction dir){
        this.data = new int[] {s1,s2};
        this.setOrientation(dir);
    }

    public int getElement(int index){
        return data[index];
    }
    
    public int[] getCoordinates() {
    	return this.data;
    }
    
    public char getOrientation() {
    	return this.orientation;
    }
    
    public void setOrientation(Direction direction) {
    	
    	char orientation = switch (direction) {
		case NORTH -> 'N';
		case SOUTH -> 'S';
		case EAST -> 'E';
		case WEST -> 'W';
		default -> 'N';
		};
		
		this.orientation = orientation;
    }
}