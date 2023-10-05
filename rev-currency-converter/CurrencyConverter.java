public class CurrencyConverter {

    public static String convert_euro(double dollar) {
        double euro = dollar * 0.92;

        return ("Euro: " + euro);
    }

    public static String convert_canada(double dollar) {
        double can = dollar * 1.36;

        return ("Canadian: " + can);
    }

    public static String convert_yen(double dollar) {
        double yen = dollar * 145.14;

        return ("Japanese Yen: " + yen);
    }

    private static String flag() {
        return "bctf{o0ps_y0u_fOuNd_mE}";

    }

}