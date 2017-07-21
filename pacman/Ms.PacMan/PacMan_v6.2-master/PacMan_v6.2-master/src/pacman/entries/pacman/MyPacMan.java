package pacman.entries.pacman;

import java.util.HashMap;
import java.util.Map;

import pacman.controllers.Controller;
import pacman.game.Constants.DM;
import pacman.game.Constants.GHOST;
import pacman.game.Constants.MOVE;
import pacman.game.Constants;
import pacman.game.Game;
import pacman.game.util.IO;


/*
 * This is the class you need to modify for your entry. In particular, you need to
 * fill in the getAction() method. Any additional classes you write should either
 * be placed in this package or sub-packages (e.g., game.entries.pacman.mypackage).
 */
public class MyPacMan extends Controller<MOVE>
{
	private MOVE myMove=MOVE.DOWN;
	private DecisionNode[] decisionNodeTree = populateTree("rules.txt");
	
	
	public MOVE getMove(Game game, long timeDue) 
	{
		Map<String, Integer> GameVariables = new HashMap<String,Integer>();
		//Key for direction:
		//0 = up
		//1 = right
		//2 = down
		//3 = left
		//4 = netural
		
		//Get the following values before anything else
		// 1. Nearest Ghost Direction ! - DEPRECATED
		// 2. Nearest Ghost Distance !
		// 3. Nearest Pill Direction ! - DEPRECATED
		// 4. Nearest Pill Distance ! - DEPRECATED
		// 5. Nearest Power Pill Direction ! 
		// 6. Nearest Power Pill Distance ! - DEPRECATED
		// 7. For each ghost (x4): !
		//    -  7.1 Ghost Edible Time
		//    -  7.2 Ghost Distance
		//    -  7.3 Ghost Direction - DEPRECATED
		
		//Get current pacman node
		int currentNode = game.getPacmanCurrentNodeIndex();
		
		//ghost distances/nodes
		int inkyNode = game.getGhostCurrentNodeIndex(GHOST.INKY);
		int inkyDist = game.getManhattanDistance(currentNode, inkyNode );
		int blinkyNode = game.getGhostCurrentNodeIndex(GHOST.BLINKY);
		int blinkyDist = game.getManhattanDistance(currentNode, blinkyNode);
		int pinkyNode = game.getGhostCurrentNodeIndex(GHOST.PINKY);
		int pinkyDist = game.getManhattanDistance(currentNode, pinkyNode);
		int sueNode = game.getGhostCurrentNodeIndex(GHOST.SUE);
		int sueDist = game.getManhattanDistance(currentNode, sueNode);
		
		//ghost edible times
		int inkyTime = game.getGhostEdibleTime(GHOST.INKY);
		int blinkyTime = game.getGhostEdibleTime(GHOST.BLINKY);
		int pinkyTime = game.getGhostEdibleTime(GHOST.PINKY);
		int sueTime = game.getGhostEdibleTime(GHOST.SUE);
		
		//nearest ghost distance/node
		int nearestGhostDist = 0;
		int nearestGhostNode = 0;
		if(sueDist < pinkyDist && sueDist < blinkyDist && sueDist < inkyDist){
			nearestGhostDist = sueDist;		
			nearestGhostNode = sueNode;
		}
		else if(pinkyDist < blinkyDist && pinkyDist < inkyDist && pinkyDist < sueDist){
			nearestGhostDist = pinkyDist;
			nearestGhostNode = pinkyNode;
		}
		else if(blinkyDist < inkyDist && blinkyDist < pinkyDist && blinkyDist < sueDist){
			nearestGhostDist = blinkyDist;
			nearestGhostNode = blinkyNode;
		}
		else{
			nearestGhostDist = inkyDist;
			nearestGhostNode = inkyNode;
		}
		
		// #4
		int nearestPillNode = game.getClosestNodeIndexFromNodeIndex(currentNode, game.getActivePillsIndices(), DM.MANHATTAN);
		int nearestPillDist = game.getManhattanDistance(currentNode, nearestPillNode);		
		// #6		
		int nearestPowerPillNode = game.getClosestNodeIndexFromNodeIndex(currentNode, game.getActivePowerPillsIndices(), DM.MANHATTAN);
		int nearestPowerPillDist = game.getManhattanDistance(currentNode, nearestPowerPillNode);
		
		
		
		//do stuff
		//with trees
		//   _____
		//  /     \
		//  |     |
		//  \__  _/
		//    \\//
		//     ||
		//     ||
		//     ||
		//     ||
		//    //\\k
		// Its a tree!
		GameVariables.put("nearestGhostDist", nearestGhostDist);
		GameVariables.put("nearestGhostNode", nearestGhostNode);
		GameVariables.put("nearestPillDist", nearestPillDist);
		GameVariables.put("nearestPillNode", nearestPillNode);
		GameVariables.put("nearestPowerPillDist", nearestPowerPillDist);
		GameVariables.put("nearestPowerPillNode", nearestPowerPillNode);
		GameVariables.put("inkyTime", inkyTime);
		GameVariables.put("blinkyTime", blinkyTime);
		GameVariables.put("pinkyTime", pinkyTime);
		GameVariables.put("sueTime", sueTime);
		GameVariables.put("inkyNode", inkyNode);
		GameVariables.put("blinkyNode", blinkyNode);
		GameVariables.put("pinkyNode", pinkyNode);
		GameVariables.put("sueNode", sueNode);

		String result = this.decisionNodeTree[0].EvalTree(GameVariables, decisionNodeTree);
		System.out.println(result);
		if(result.charAt(0) == 'S'){
			myMove = game.getNextMoveTowardsTarget(currentNode, GameVariables.get(result.substring(1)), DM.MANHATTAN);
		}
		else
			myMove = game.getNextMoveAwayFromTarget(currentNode, GameVariables.get(result.substring(1)), DM.MANHATTAN);
		
		
		System.out.println(myMove.toString());
		return myMove;
			
	}
	

	
	//
	//Populates a decision node tree
	public DecisionNode[] populateTree(String fileName){
		//Load the file using given filename, split on newline, add to string array
		String fileData = IO.loadFile(fileName);
		String[] ruleList = fileData.split("\n");
		//Create tree of size of rulelist
		DecisionNode[] theTree = new DecisionNode[ruleList.length];
		//For each rule in the rulelist, create a new decisionnode by passing the rule string into the constructor
		for(int i = 0; i < ruleList.length; i++){
			theTree[i] = new DecisionNode(ruleList[i]);
		}
		//Return the root of the tree
		return theTree;		
	}
	

	
	
	public class Condition
	{
		String leftHandSide  = "";
		String rightHandSide = "";
		String operator = "";
		
		public Condition(String lhs, String op, String rhs)
		{
			leftHandSide = lhs;
			rightHandSide = rhs;
			operator = op;
		}
		public boolean Eval(Map<String,Integer> Vars)
		{
			int lhsValue = Vars.get(leftHandSide);
			int rhsValue;
			try{
				rhsValue = Integer.parseInt(rightHandSide);
			}
			catch(Exception ex){
				rhsValue = Vars.get(rightHandSide);
			}
			
			if(operator.equals("!="))
				return lhsValue != rhsValue;
			
			else if(operator.equals("=="))
				return lhsValue == rhsValue;
			
			else if(operator.equals("<="))
				return lhsValue <= rhsValue;
			
			else if(operator.equals(">="))
				return lhsValue >= rhsValue;
			
			else if(operator.equals("<"))
				return lhsValue < rhsValue;
			
			else if(operator.equals(">"))
				return lhsValue > rhsValue;
			
			return false;
		}
	}

	public class DecisionNode
	{
		public Integer label;
		public Condition cond;
		public String left;
		public String right;
		
		
		public DecisionNode(String rule)
		{
			String[] splitRule = rule.split("-");
			this.label = Integer.parseInt(splitRule[0]);
			String[] splitCond = splitRule[1].split("_");
			this.cond = new Condition(splitCond[0],splitCond[1],splitCond[2]);
			this.left = splitRule[2];
			this.right = splitRule[3];
		}
		public String EvalTree(Map<String,Integer> Vars,DecisionNode theTree[])
		{
			int temp = 0;
			if(this.cond.Eval(Vars) == true)
			{
				try{
					temp = Integer.parseInt(left);
					return theTree[temp].EvalTree(Vars,theTree);
				}
				catch(Exception ex)
				{
					return left;
				}
			}
			else
			{
				try{
					temp = Integer.parseInt(right);
					return theTree[temp].EvalTree(Vars,theTree);
				}
				catch(Exception ex)
				{
					return right;
				}
			}
		}
	}
}