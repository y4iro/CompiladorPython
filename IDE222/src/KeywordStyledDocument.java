
import java.awt.Color;
import javax.swing.text.AttributeSet;
import javax.swing.text.BadLocationException;
import javax.swing.text.DefaultStyledDocument;
import javax.swing.text.Style;
import javax.swing.text.StyleConstants;
import javax.swing.text.StyleContext;

public class KeywordStyledDocument extends DefaultStyledDocument {

    private final Style S_default;
    private final Style S_PalabraReservada;
    private final Style S_Numeros;
    private final Style S_CaracterEspecial;
    private final Style S_Identificadores;
    private final Style S_Comentarios;

    public KeywordStyledDocument() {

        StyleContext styleContext = new StyleContext();
        S_default = styleContext.getStyle(StyleContext.DEFAULT_STYLE);
        Style cwStyle = styleContext.addStyle("ConstantWidth", null);
        StyleConstants.setForeground(cwStyle, Color.BLACK);
        StyleConstants.setBold(cwStyle, true);

        StyleContext C_PalabraReservada = new StyleContext();
        S_PalabraReservada = C_PalabraReservada.addStyle("ConstantWidth", null);
        StyleConstants.setForeground(S_PalabraReservada, new Color(40, 88, 202));
        StyleConstants.setBold(S_PalabraReservada, true);

        StyleContext C_Numero = new StyleContext();
        S_Numeros = C_Numero.addStyle("ConstantWidth", null);
        StyleConstants.setForeground(S_Numeros, new Color(237, 70, 47));
        StyleConstants.setBold(S_Numeros, true);

        StyleContext C_CaracterEspecial = new StyleContext();
        S_CaracterEspecial = C_CaracterEspecial.addStyle("ConstantWidth", null);
        StyleConstants.setForeground(S_CaracterEspecial, new Color(74, 151, 22));
        StyleConstants.setBold(S_CaracterEspecial, true);

        StyleContext C_Identificadores = new StyleContext();
        S_Identificadores = C_Identificadores.addStyle("ConstantWidth", null);
        StyleConstants.setForeground(S_Identificadores, new Color(203, 138, 48));
        StyleConstants.setBold(S_Identificadores, true);

        StyleContext C_Comentarios = new StyleContext();
        S_Comentarios = C_Comentarios.addStyle("ConstantWidth", null);
        StyleConstants.setForeground(S_Comentarios, new Color(150, 150, 150));
        StyleConstants.setBold(S_Comentarios, true);
    }

    @Override
    public void insertString(int offset, String str, AttributeSet a) throws BadLocationException {
        super.insertString(offset, str, a);
        refreshDocument();
    }

    @Override
    public void remove(int offs, int len) throws BadLocationException {
        super.remove(offs, len);
        refreshDocument();
    }

    private synchronized void refreshDocument() throws BadLocationException {

        // FORMATOS GENERALES
        String text = getText(0, getLength());
        paint(0, text.length(), S_default);
        int index, index2;

        // VALIDACIÓN COMPLETA PARA PINTAR
        for (index = 0; index < text.length(); index++) {

            // COMENTARIOS 1 LINEA
            if ((index < text.length() - 1) && text.charAt(index) == '/' && text.charAt(index + 1) == '/') {
                String[] cut = text.substring(index).split("\n");
                paint(index, cut[0].length(), S_Comentarios);
                index += cut[0].length();

                // COMENTARIOS MULTIPLES LINEAS
            } else if ((index < text.length() - 1) && text.charAt(index) == '/' && text.charAt(index + 1) == '*') {
                boolean closed = false;
                for (index2 = index + 2; index2 < text.length() - 1; index2++) {
                    if (text.charAt(index2) == '*' && text.charAt(index2 + 1) == '/') {
                        paint(index, index2 - index + 2, S_Comentarios);
                        index = index2 + 1;
                        closed = true;
                        break;
                    }
                }
                if (!closed) {
                    paint(index, text.length() - index, S_Comentarios);
                    index = text.length();
                }

                // IDENTIFICADOR
            } else if (Character.isLetter(text.charAt(index))) {
                index2 = index + 1;
                while (index2 < text.length() && (Character.isDigit(text.charAt(index2)) || Character.isLetter(text.charAt(index2)) || text.charAt(index2) == '_')) {
                    index2++;
                }
                paint(index, index2 - index, S_Identificadores);

                //PALABRA RESERVADA
                String word = "";
                for (int i = index; i < index2; i++) {
                    word += text.charAt(i);
                }
                if (word.equals("main") || word.equals("if") || word.equals("then")
                        || word.equals("else") || word.equals("end") || word.equals("do")
                        || word.equals("while") || word.equals("repeat") || word.equals("until")
                        || word.equals("cin") || word.equals("cout") || word.equals("real")
                        || word.equals("int") || word.equals("boolean")) {
                    paint(index, index2 - index, S_PalabraReservada);
                }
                index = index2 - 1;

                // NÚMERO
            } else if (Character.isDigit(text.charAt(index))) {
                index2 = index + 1;
                while (index2 < text.length() && Character.isDigit(text.charAt(index2))) {
                    index2++;
                }
                if (text.charAt(index2) == '.') {
                    index2++;
                    if (Character.isDigit(text.charAt(index2))) {
                        while (index2 < text.length() && Character.isDigit(text.charAt(index2))) {
                            index2++;
                        }
                        paint(index, index2 - index, S_Numeros);
                        index = index2 - 1;
                    }
                } else {
                    paint(index, index2 - index, S_Numeros);
                    index = index2 - 1;
                }
            }else if( (text.charAt(index) == ')' || text.charAt(index) == '(' || text.charAt(index) == '{' || text.charAt(index) == '}') ){
                paint(index, 1, S_CaracterEspecial);
            }

        }
    }
    
    private void paint(int position, int length, Style style) {
        setCharacterAttributes(position, length, style, true);
    }

}
