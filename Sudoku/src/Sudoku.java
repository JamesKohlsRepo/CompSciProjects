import java.util.Arrays;

public class Sudoku {

	public static void main(String args[]) {
		int rowCount = 0;
		
		int[][] sudokuBoard = new int[9][9];
		int[] ranGeneration = {1,2,3,4,5,6,7,8,9};   
		
		
		for(int i = 0; i < ranGeneration.length; i++) {
			int rand = 0;
			rand = (int)(Math.random() * 9);
			int temp = ranGeneration[rand];
			
			ranGeneration[rand] = ranGeneration[i];
			ranGeneration[i] = temp;
		}
		
		
		
		System.out.println(Arrays.toString(ranGeneration));
		
		System.out.println();
		System.out.println();
		
		
		//selects values for each position of the board
		for(int i = 0; i < sudokuBoard.length; i++) {
			for(int j = 0; j < sudokuBoard[0].length; j++) {
				
				sudokuBoard[i][j] = 0;
				
				
				System.out.print(sudokuBoard[i][j] + " ");
				
				
				//separates each row from each other 
				rowCount +=1;
				if (rowCount % 9 == 0) {System.out.println();}
					
					
				
				
			}
			
			
		}
		
		
		
		
}
}
