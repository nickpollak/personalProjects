import java.math.BigInteger;

public class ExtendedEuclidian{

	public static void main(String[] args){
		extendedEuclidianAlg2(26, 11);
	}

	public static int extendedEuclidianAlg(int m, int n) {
		int a = n, b = m % n, c, d;
		int i = 0, j = 1;
		while (b != 0) {
			d = a / b;
			c = a - d * b;
			a = b;
			b = c;
			c = i - d * j;
			i = j;
			j = c;
		}

		if (i < 0) {
			i += n;
		}

		return i;
	}

	public static int extendedEuclidianAlg2(int n, int m){
		int left = n;
		int right = m;
		int x = 0;
		int y = 1;
		int xPrev = 1;
		int yPrev = 0;
		while(right != 0){
			int r = left % right;
			int q = left/right;

			left = right;
			right = r;

			int temp = x;
			x = xPrev - q*x;
			xPrev = temp;

			temp = y;
			y = yPrev-q*y;
			yPrev = temp;
		}
		if (x < 0) {
			x += n;
		}
		System.out.println(x + " " + y);
		return x;
	}

	// public static int ExtendedEuclidianAlg3(int n, int m){
	// 	int left = n; int right = m;
	// 	int x = 0; int xPrev = 1; int y = 1; int yPrev = 0;
	// 	int q; int qPrev; int r; int rPrev;
	// 	while(right != 0){
	// 		r = left % right;
	// 		q = left / right;




	// 		qPrev = q;
	// 		xPrev = x;
	// 		yPrev = y;
	// 		rPrev = r;
	// 	}

	// }

}