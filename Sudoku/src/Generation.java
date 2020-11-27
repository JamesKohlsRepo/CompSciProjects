import java.io.*; 
import java.util.*; 
public class Generation {

	
	public int[][] currentGeneration;
	
public Generation(int[][] currentGeneration) {
	
	this.currentGeneration = currentGeneration;
	
}

public int createRow() {
	
	int[] nextRow = new int[9];
	
	for(int i = 0; i < nextRow.length; i++) {
		int rand = 0;
		rand = (int)(Math.random() * 9);
		int temp = nextRow[rand];
		
		nextRow[rand] = nextRow[i];
		nextRow[i] = temp;
	}
	
	ArrayList<Integer> Storage = new ArrayList<Integer>(currentGeneration.length % 9); 
	
	for(int i = 0; i < 9; i ++) {
		
		for (int j = 0; j < currentGeneration.length % 9; j++){
			Storage.add(i + (9 * j));
		}
		
		if (Storage.contains(nextRow[i])){
			
			for(int x = 0; x < nextRow.length; x++) {
				
				if ((nextRow[i] == nextRow[x]) && (i != x)) {
					int temp = nextRow[rand];
					
					nextRow[rand] = nextRow[i];
					nextRow[i] = temp;
				}
				
			}
			
		}
		
}	
	
	
	
	
	return 0;
}

	
	
	
}
