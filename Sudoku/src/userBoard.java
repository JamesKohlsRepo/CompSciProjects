
public class userBoard {

	public int[][] sudokuBoard;
	
	public userBoard(int[][] sudokuBoard) {
		this.sudokuBoard = sudokuBoard;
	}
	
	public int[][] playerBoard(int[][] sudokuBoard, int difficulty){
		
		int[][] playerBoard = new int[9][9];
		
		for(int i = 0; i < sudokuBoard.length; i++) {
            for(int j = 0; j < sudokuBoard[0].length; j++) {
            	int rand = (int)(Math.random() * 100) + 1;
            	if(rand >= difficulty) { playerBoard[i][j] = 0; }
            	else { playerBoard[i][j] = sudokuBoard[i][j]; }
            }
        }
		return playerBoard;
	}
	
}
