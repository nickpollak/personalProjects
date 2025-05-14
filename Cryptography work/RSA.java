import java.util.*;
import java.util.function.BiFunction;

import javax.swing.plaf.basic.BasicToggleButtonUI;

import java.io.File;
import java.io.FileNotFoundException;
import java.math.BigInteger;

public class RSA {

    public static void main(String[] args){
        ArrayList<BigInteger> blocks = new ArrayList<BigInteger>();
        BigInteger e = new BigInteger("4176633317755433431678678465889845648936806464054866324801744270342879044357669071538839129364698164188798225568335994640432560988356730693851317935746877161305651215590558294715565265787259928455687779275518989163716278946174842872593308106774329128648241556306020338325508704527416130688489628415582686345635693623358474263275478962412758022516421325101632609820589933809050550757747025490064609998396350574372258369895583579424232259743356143849915773687015194184717679321087404939363733716866682044749344859345372083518644958446399833747002184853693942701921082639972060795990236397154101820908184629901054840663");
        BigInteger n = new BigInteger("14298181905606428347627867110585917348912683448698978471804729574373779858086632467238799069649901576504916566304536661705268080039971945507404314082440363737497962776748827332482389599283969278800550813823873063435132684378328939822815610184019316982015941901886112691184498349051766454836272673177203307545214590830176163386832720647098168334761696461462847810619080847797532047942838579638498302905904892859844751396170672344434048027879329595548282317278534435515026753427827313841328736451206675985752448738124499752171280428574482710417865608895117382309990899824941382269138221052659161841874082502923516327369");
        BigInteger d = new BigInteger("14002174790121783527288317630633164782209207260104997127596659484324683118954544207658545438928308614624419863541136955007512796926197426499840625873197484771163080886647676848153799823249517091727012292596320959149870939248303455680519758666308748236028811332568509339757761177088926065655620436927894316342612758396654539591543545516197467073501771253743377392282456643176883428862584939110553805839174462698718516603826745188004031053048627181817201882415757647925188703809521827024454659375537475317917491255570890824686753321650475963802717179884502587047508924109849803332503937781591334750730252315897935894375");
        //add a scanner for file name maybe
        File fileInput = new File("/Users/nickpollak/Desktop/Cryptography/text.txt");
        String message = "";
        try {
            Scanner input = new Scanner(fileInput);
            message += input.nextLine();
            System.out.println("message: " + message);
            while(message != ""){
                if(message.length() > 214){
                    String temp = "";
                    int i = 0;
                    while(i < 214){
                        temp += (byte) message.charAt(0);
                        message = message.substring(1, message.length());
                        i++;
                    }
                    blocks.add(new BigInteger(temp));
                }else{
                    String temp = "";
                    int i = 0;
                    int len = message.length();
                    while(i < len){
                        temp += (byte) message.charAt(0);
                        message = message.substring(1, message.length());
                        i++;
                    }
                    blocks.add(new BigInteger(temp));
                }
            }
            input.close();
            } catch (FileNotFoundException f) {
                f.printStackTrace();
            }
        
        

        ArrayList<BigInteger> enc = rsaEncrypt(blocks, e, n);
        ArrayList<BigInteger> dec = rsaDecrypt(enc, d, n);
        System.out.println(numsToLetters(dec));
    }

    public static ArrayList<BigInteger> rsaEncrypt(ArrayList<BigInteger> blocks, BigInteger e, BigInteger n){
        System.out.println("ENCRYPTED: ");
        ArrayList<BigInteger> encrypted = new ArrayList<BigInteger>();
        for(int i = 0; i < blocks.size(); i++){
            BigInteger temp = blocks.get(i).modPow(e,n);
            System.out.print(temp);
            encrypted.add(temp);
        }
        System.out.println();
        return encrypted;
    }

    public static ArrayList<BigInteger> rsaDecrypt(ArrayList<BigInteger> cipher, BigInteger d, BigInteger n){
        System.out.println("DECRYPTED: ");
        ArrayList<BigInteger> decrypted = new ArrayList<BigInteger>();
        for(int i = 0; i < cipher.size(); i++){
            BigInteger temp = cipher.get(i).modPow(d,n);
            System.out.print(temp);
            decrypted.add(temp);
        }
        System.out.println();
        return decrypted;
    }

    public static String numsToLetters(ArrayList<BigInteger> blocks){
        System.out.println("MESSAGE: ");
        String orgMessage = "";
        String temp = "";
        int holder;
        for(int i = 0; i < blocks.size(); i++){
            temp = blocks.get(i).toString(0);
            while(!temp.isEmpty()){
                holder = Integer.valueOf(temp.substring(0,2));
                orgMessage += (char)holder;
                temp = temp.substring(2,temp.length());
            }
        }
        return orgMessage;
    }
}


