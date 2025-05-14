import java.math.BigInteger;
import java.util.*;

public class secondPreview extends ExtendedEuclidian{
    public static void main(String[] args){
        Scanner input = new Scanner(System.in);
        // System.out.println("Enter the key: ");
        // String key = (input.nextLine()).toLowerCase();
        // System.out.println("Enter the message: "); 
        // String plaintext = (input.nextLine()).toLowerCase();
        //System.out.println("Enter the cipher: "); 
        //String cipher = (input.nextLine()).toUpperCase();
        //System.out.println(orderOfElements(7,9));
        //System.out.println(totientFunc(125));
        //System.out.println(chineseRemainder(4,3, 77));
        //System.out.println(findInverse(7457, 11200));
        //System.out.println(sophieGermainP());
        //System.out.println(orderOfElements(7, 359));
        //System.out.println(bruteForceAffineDecrypt("BHKTGIKFVKIIGLRKPAFSXYLFVPMZBIVFOBRRGGDTVPQFYGKIOPGOHKPFTYERWAPLGZFZTNIPLKKVRCGFXFSFWJTYPAFGXCRUNZBYPBJGJAXAWXYVIDKTGPIOCTOXIPTBPBVGGDNGZEFZNCCOWQKHRLFAYEIGLRGPVXAZZJIOHHMBXPFWXAXAWXYMGNFLUPRPPGKLWWFKRBRTJOTUKTGRGPWAJSNYCKSFOATKGLRGUETTLMVOXTYCRBKGWNRGLRKAVIWXKLAFWKZBFKTIDAEEDXZJMEWTYRESOMGLIKKWVRRMTIUWKKGATYPPJDIQMIDBRNZXFDNGVELGXQRBOMTIRLFSXRPLWXNCAZLNKKGNJKGHHKSHXAMZZDTAWGFCOJPOHNUERRHBKGRMZOTUBMJYHLQZJRZUVKOWVYRCMCZPJQFUTCRPBMZBIKKHKEWSFPUTVKGAHLPJJMUHIKGTXGLXFCZCZEFOTQLBHKTVIKDWFVRZTXOPVAFKTMJOPGKGRFFGRNPEFLKPTMMMNGRHXMGHHKKCXVXGOSRNVNWTGQRJBMGFPKLVOAWMSBYPEQJKTJEVCGOHKWFKRRRGQYAPTAGQTYXOPGKHWHQBKGRGAQNV"));
        // String [] a = bruteForceShiftDecrypt("BHKTGIKFVKIIGLRKPAFSXYLFVPMZBIVFOBRRGGDTVPQFYGKIOPGOHKPFTYERWAPLGZFZTNIPLKKVRCGFXFSFWJTYPAFGXCRUNZBYPBJGJAXAWXYVIDKTGPIOCTOXIPTBPBVGGDNGZEFZNCCOWQKHRLFAYEIGLRGPVXAZZJIOHHMBXPFWXAXAWXYMGNFLUPRPPGKLWWFKRBRTJOTUKTGRGPWAJSNYCKSFOATKGLRGUETTLMVOXTYCRBKGWNRGLRKAVIWXKLAFWKZBFKTIDAEEDXZJMEWTYRESOMGLIKKWVRRMTIUWKKGATYPPJDIQMIDBRNZXFDNGVELGXQRBOMTIRLFSXRPLWXNCAZLNKKGNJKGHHKSHXAMZZDTAWGFCOJPOHNUERRHBKGRMZOTUBMJYHLQZJRZUVKOWVYRCMCZPJQFUTCRPBMZBIKKHKEWSFPUTVKGAHLPJJMUHIKGTXGLXFCZCZEFOTQLBHKTVIKDWFVRZTXOPVAFKTMJOPGKGRFFGRNPEFLKPTMMMNGRHXMGHHKKCXVXGOSRNVNWTGQRJBMGFPKLVOAWMSBYPEQJKTJEVCGOHKWFKRRRGQYAPTAGQTYXOPGKHWHQBKGRGAQNV");
        // for(int i = 0; i < a.length; i++){
        //     System.out.println(a[i]);
        // }
        //System.out.println(findInverse(25679, 35209));
        //System.out.println(allOrders(822));
        bruteForceShiftDecrypt("MWVAYWRMJUUQIPDHNXYGAYZRVPTSAPVBJHGBHLJGWDZNVGWMTNBZIGJJPKWHDEGDUCSAJBFLBKGCIDLHNRQLSWGIRFWUUUWTTRDINMHDXPIQBKGKAVTWJIKPFKXMYXHQPBEVCIDLDVRKQHWMKIFUKNIXCAGBBCKIKPWUBYYRECHXNDHTTWUBZKICGOBODMATFMHIVCPQEMWVAYWRKQLQVYFYNJNCMYIDMOZBOPWIVYINEDUPGOMOQGYRKBNTCIDDSSEWHOQJZEKMOMNAQIAEKTEDOFWZRTXOYSTEJPQKIRRZVKCBSBFNPPIPFGJBAZBXBUIVHTTTKOJUEXTRGZCHWTBODEWACIDUWZKIUYIDSMJDOFURHREXPDEBHZQVUOVHCKNFAMCIDMGFJDQCCGCIDAJNAPYSMKTGHQYZNACJGYKMETTPQMFMFBADQLPWGWLGICWMZHZRAQWRZNPCQ");
        input.close();
    }

    public static long sophieGermainP(){
        boolean found = false;
        long i = (long)Math.pow(10, 20) + 1;
        while(!found){
            if(isPrime(i) && isPrime(i*2 + 1)){
                found = true;
            }else{
                i = i + 2;
            }
        }
        return i;
    }

    public static boolean isPrime(long n){
        if(n <= -1){
            return false;
        }else{
            for(int i = 2; i < n/2; i++){
                if(n%i == 0){
                    return false;
                }
            }
        }
        return true;
    }

    public static String encryptShift(String k, String m){
        String result = "";
        m = m.replaceAll(" ", "");
        for(int i = 0; i < m.length(); i++){
            int shift = k.charAt(i%k.length()) - 'a';
            int fixer = ((m.charAt(i) + shift - 'a') % 26) + 'a';
            result += (char)fixer;
        }
        System.out.println("\n" + result);
        return result;
    }

    public static String decryptShift(String k, String c){
        String result = "";
        c = c.replaceAll(" ", "");
        for(int i = 0; i < c.length(); i++){
            int shift = c.charAt(i) - 'A';
            char fixer = (char)((shift - (k.charAt(i % k.length()) - 'a') + 26) % 26 + 'a');
            result += fixer;
        }
        //System.out.println("\n" + result.toLowerCase());
        return result.toLowerCase();
    }

    public static String affineEncrypt(String m, int a, int b){
        String res = "";
        for(int i = 0; i < m.length(); i++){
            res += (char)((((a * (m.charAt(i) - 'a')) + b) % 26) + 'A');
        }
        return res;
    }

    public static String affineDecrypt(String c, int a, int b){
        String res = "";
        for(int i = 0; i < c.length(); i++){
            res += (char)(((((c.charAt(i) - 'A' - b + 26)% 26) * findInverse(a, 26)) % 26) + 'a');
        }
        return res;
    }

    public static String bruteForceAffineDecrypt(String c){
        double moicMax = 0;
        int aPos = 0;
        int bPos = 0;
        //all possible a values: 1 to 25 multiplying by 26 is the same as 1
        for(int a = 1; a < 26; a++){
            //all possible b values: 1 to 25 adding 26 is the same as adding 0
            for(int b = 1; b < 26; b++){
                double moicCur = mututalIndexOfCoincidence(freqFinder(affineDecrypt(c, a, b)));
                if( moicCur > moicMax && moicCur < .07){
                    System.out.println(moicMax);
                    moicMax = mututalIndexOfCoincidence(freqFinder(affineDecrypt(c, a, b)));
                    System.out.println(moicMax);
                    aPos = a;
                    bPos = b;
                }
            }
        }
        return affineDecrypt(c, aPos, bPos);
    }

    public static double[] freqFinder(String m){
        m = m.replaceAll(" ", "");
        m = m.toUpperCase();
        double[] freqs = new double[26];
        for(int i = 0; i < m.length(); i++){
            freqs[(m.charAt(i) - 'A')] += 1;
        }
        for(int j = 0; j < freqs.length; j++){
            freqs[j] = freqs[j]/m.length();
        }
        return freqs;
    }

    public static void printFreqs(String m, double [] a){
        for(int i = 0; i < a.length; i++){
            System.out.print((char)(i + 'A') + ":" + (a[i] + " "));
        }
    }

    public static double indexOfCoincidence(double[] f){
        double ioc = 0;
        for(double i : f){
            ioc += i*i;
        }   
        System.out.println("Index Of Coindidence: " + ioc);
        return ioc;
    }

    public static double mututalIndexOfCoincidence(double[] f){
        double mioc = 0;
        for(int i = 0; i < f.length; i++){
            mioc += f[i] *  ENGLISH_FREQ[i];
        }
        //System.out.println("Mutual Index Of Coindidence: " + mioc); 
        return mioc;
    }

    public static String [] bruteForceShiftDecrypt(String c){
        String [] results = new String[26];
        for(int i = 0; i < 26; i++){
            String newK = "";
            newK += (char)(i + 'a');
            results[i] = decryptShift(newK, c);
        }
        System.out.println(mututalIndexOfCoincidence(freqFinder(results[26])));
        return results;
    }

    public static void multTable(int n){
        for(int i =0; i < n; i++){
            System.out.print(i + ": ");
            for(int j =0; j < n; j++){
                System.out.print(((i*j) % n) + " ");
            }
            System.out.println();
        }
    }

    public static int orderOfElements(int a, int b){
        int order = 1;
        while((Math.pow(a, order)) % b != 1){
            order = order + 1;
        }
        return order;
    }

    public static ArrayList<Integer> allOrders(int n){
        ArrayList<Integer> a = new ArrayList<Integer>(); 
        for(int i = 0; i < n; i++){
            if(orderOfElements(i, n) != n-1){
                a.add(i);
            }
        }
        return a;
    }

    public static int findInverse(int a, int b){
        for(int i = 1; i < b; i++){
            if((a*i) % b == 1){
                return i;
            }
        }
        return -1;
    }

    public static int chineseRemainder(int a, int b, int m){
        //Works great finds the prime factorizations
        int x = 0;
        int m1 = 0;
        int m2 = 0;
        for(int i = 3; i < m/2; i+=2){
            if(m % i == 0){
                if(m1 == 0){
                    m1 = i;
                    System.out.println(m1);
                }else{
                    if(gcd(m1, i) == 1){
                        m2 = i;
                        System.out.println(m2); 
                    } 
                }
            }
        }
        int t = extendedEuclidianAlg(m1, m2);
        System.out.println(t);
        x = (Math.abs((t * m2 * b) - (t * m1 * a))) % m;
        return x;
    }

    public static int totientFunc(int a){
        int count = 0;
        for(int i = 1; i < a; i++){
            if(findInverse(i, a) != 0){
                count++;
            }
        }
        return count;
    }

    public static int findKeyLen(String c){
        int displacementMax = 1;
        double coincidenceMax = 0;
        //loop thru all possible displacements i
        for(int i = 1; i < c.length()/5; i++){
            double coincidenceCur = 0;
            //finds coincidences for a specific displacement while j is the iterative variable from 0
            //to c.length - i
            int j = 0;
            while(j + i < c.length()){
                if(c.charAt(j) == c.charAt(j + i)){
                    coincidenceCur += 1;
                }
                j++;
            }
            if(coincidenceCur > coincidenceMax && (i % displacementMax != 0 || i < 9)){
                coincidenceMax = coincidenceCur;
                System.out.println(displacementMax);
                displacementMax = i;
                System.out.println(displacementMax);
            }
        }
        return displacementMax;
    }

    public static String cipherKeyDecrypt(String m){
        String decryptedKey = "";
        int len = findKeyLen(m);
        double [] moics = new double[len];
        String [] partitions = new String[len];
        for(int i = 0; i < m.length(); i++){
            partitions[i%len] += m.charAt(i);
        }
        System.out.println("Mutual Idexes: ");
        for(int x = 0; x < len; x++){
            //then compare that moic to moic[x] if its greater keep it
            int shift = 0;
            //I think my results might get messed up by my mutualIndexes because it thinks the length
            //Is longer than it is
            for(int j = 0; j < 26; j++){
                double temp = mututalIndexOfCoincidence(freqFinder(bruteForceShiftDecrypt(partitions[x])[j]));
                if(temp > moics[x]){
                    moics[x] = temp;
                    shift = j;
                }
            }
            decryptedKey += (char)(shift + 'a');
            System.out.print(moics[x] + ", ");
        }
        System.out.println();
        return decryptedKey;
    }

    public static int gcd(int m, int n){
        if(n==0){
            return m;
        }
        return gcd(n, m%n);
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

    final static double[] ENGLISH_FREQ = {
        0.082,0.015,0.028,0.043,0.127,0.022,0.020,0.061,0.070,0.002,0.008,0.040,0.024,0.067,0.075,0.019,
        0.001,0.060,0.063,0.091,0.028,0.010,0.023, 0.001,0.020,0.001
    };


}
