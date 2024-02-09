package mdp.g18.sim;

import java.util.ArrayList;

public class Node implements Comparable<Node>{
	private double g;
	private double f;
	private double h;
	private char direction;
	private int[] coord;
	private int obstacleID; // -1 if robot
	public ArrayList<Edge> neighbour = new ArrayList<>();

	private Node parent;
	private boolean visited;

	Node(double g, int[] coord, Node parent, int id) {
		this.g = g;
		this.coord = coord;
		this.parent = parent;
		this.obstacleID = id;
	}

	public double getG() {
		return g;
	}

	public void setG (double g){
		this.g = g;
	}
	
	public double getF() {
		return f;
	}

	public void setF (double f){
		this.f = f;
	}
	
	public double getH() {
		return h;
	}

	public void setH (double h){
		this.h = h;
	}
	
	public char getDirection() {
		return direction;
	}

	public void setDirection (char dir){
		this.direction = dir;
	}

	public boolean isVisited() { return visited; }

	public void setVisited(boolean visited) { this.visited = visited; }

	public int[] getCoord() {
		return this.coord;
	}

	public void setCoord(int[] coord) {
		this.coord = coord;
	}

	public Node getParent() {
		return parent;
	}

	public void setParent(Node parent) {
		this.parent = parent;
	}

	public int getObstacleID() {
		return this.obstacleID;
	}

	public void setNeighbour(ArrayList<Edge> neighbour) {
		this.neighbour = neighbour;
	}

	public double calculateH(Node current, Node target) {
		double x = Math.abs(current.getCoord()[0] - target.getCoord()[0]);
		double y = Math.abs(current.getCoord()[1] - target.getCoord()[1]);
		return Math.sqrt(Math.abs(Math.pow(x, 2) + Math.pow(y, 2)));
	}

	@Override
	public int compareTo(Node o) {
		if (this.getG() > o.getG()) {
			return 1;
		} else if (this.getG() < o.getG()) {
			return -1;
		}
		return 0;
	}
	
	public static class Edge {
        Edge(int weight, Node node){
              this.weight = weight;
              this.node = node;
        }

        public int weight;
        public Node node;
	}
}