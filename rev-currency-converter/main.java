import java.io.Console;

public class main {

    public static void main(String[] args) {

        Console in = System.console();

        System.out.println("How much are you converting?\n");
        String str = in.readLine();
        double dollar = Double.parseDouble(str);
        System.out.println("What would you like to convert to? 1:Euro, 2:Canadian, 3:Yen\n");
        String choice = in.readLine();

        switch (choice) {
            case "1":
                System.out.println(CurrencyConverter.convert_euro(dollar));
                break;
            case "2":
                System.out.println(CurrencyConverter.convert_canada(dollar));
                break;
            case "3":
                System.out.println(CurrencyConverter.convert_yen(dollar));
                break;
        }

    }

}
