import java.math.BigInteger;

public class exponentModulus {
   
    public static void main(String[] args){
        // System.out.println(finalRem(5859, 5793, 11413));
        // System.out.println(finalRem(2, 10203, 101));
        // System.out.println(fermatLiarCount(1147));
        //System.out.println(isQuadRes(2123, 4831));
        //System.out.println(jacobiSymb(8, 21));
        //System.out.println(isQuadRes(79, 1117));
        BigInteger a = new BigInteger("55146139");
        BigInteger n = new BigInteger("56052361");
        BigInteger res = a.modPow(new BigInteger("28026180"), n);
        System.out.println(res);
    }

    public static int[] binaryRep(int n){
        int [] binary = new int[32];
        int pos = 31;
        while(n > 0){
            binary[pos--] = n % 2;
            n = n/2;
        }
        return binary;
    }

    public static int finalRem(int a, int ex, int m){
        int [] bin = binaryRep(ex);
        int finModulus = 1;
        int prevMod = a % m;
        int curMod;
        //couldn't figure out how to get the first one without messing up my loop
        if(bin[bin.length-1] != 0){
            finModulus = finModulus * prevMod;
        }
        //loops from the 2's position in binary to the last spot
        for(int i = bin.length - 2; i >= 0; i--){
            curMod = (int)(Math.pow(prevMod, 2) % m);
            prevMod = curMod;
            if(bin[i] != 0){
                finModulus = (finModulus * curMod) % m;
            }
        }
        return finModulus;
    }

    public static int fermatLiarCount(int p){
        int count = 2;
        for(int i = 2; i < p -1; i++){
            if(finalRem(i, p-1, p) == 1){
                count++;
            }
        }
        return count;
    }

    public static boolean isQuadRes(int a, int p){
        if(finalRem(a, (p-1)/2, p) == 1){
            return true;
        }
        return false;
    }

    public static int jacobiSymb(int a, int p){
        int b = a % p;
        //check if it is finished finding 1, 0, -1
        if(b == 1 || b == 0 || b == -1){
            return b;
        }
        else{
            //first check if odd or even
            if(b % 2 == 0){
                if(p % 8 == 1 || p % 8 == 7){
                    b = b/2;
                    return jacobiSymb(b, p);
                }else if(p % 8 == 3 || p % 8 == 5){
                    b = (-1 * b)/2;
                    return jacobiSymb(b, p);
                }
            }else{
                if(gcd(b, p) == 1){
                    if(b % 4 == 3 && p % 4 == 3){
                        return jacobiSymb(-p, b);
                    }else{
                        return jacobiSymb(p, b);
                    }
                }
            }
            return b;
        }
    }

    public static int gcd(int m, int n){
        if(n==0){
            return m;
        }
        return gcd(n, m%n);
    }

}
