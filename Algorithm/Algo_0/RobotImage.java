package mdp.g18.sim;

import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.geom.AffineTransform;
import java.awt.image.BufferedImage;
import java.io.IOException;

import javax.imageio.ImageIO;

public class RobotImage {
	
	private final static int RADIUS = Robot.ROBOT_SIZE * Arena.UNIT_SIZE;
	
	BufferedImage robotImage;
	
	RobotImage(int x, int y, Direction direction){	
		try{
	        robotImage = ImageIO.read(getClass().getResource("/Resources/robot.png"));
	        robotImage = resizeImage(robotImage, RADIUS, RADIUS);
	    }catch(IOException e){e.printStackTrace();}
	    catch(Exception e){e.printStackTrace();}
	}
	
	private BufferedImage resizeImage(BufferedImage originalImage, int targetWidth, int targetHeight) throws IOException {
	    BufferedImage resizedImage = new BufferedImage(targetWidth, targetHeight, BufferedImage.TYPE_INT_RGB);
	    Graphics2D graphics2D = resizedImage.createGraphics();
	    graphics2D.drawImage(originalImage, 0, 0, targetWidth, targetHeight, null);
	    graphics2D.dispose();
	    return resizedImage;
	}
	
	// Draw robot with center coordinates of robot
	public void drawRobot(Graphics g, int x, int y, Direction direction){
		
		int angle = switch (direction) {
		case NORTH -> angle = 0;
		case SOUTH -> angle = 180;
		case EAST -> angle = 90;
		case WEST -> angle = -90;
		default -> angle = 0;
		};
		
		Graphics2D g2 = (Graphics2D) g;
        AffineTransform at = new AffineTransform();
        at.translate( x * Arena.UNIT_SIZE + Arena.UNIT_SIZE, Arena.ARENA_HEIGHT + y * Arena.UNIT_SIZE - Arena.UNIT_SIZE);
        at.rotate(Math.toRadians(angle));
        at.translate(-RADIUS/2,-RADIUS/2);
        g2.drawImage(robotImage, at, null);
	}
}