
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import javax.swing.JTextArea;

public class Terminal extends Thread{
    public JTextArea terminal;
    public String str="";
    protected BufferedWriter writer;
    protected BufferedReader reader;
    protected String answer;
    public Terminal(JTextArea terminal){
        this.terminal=terminal;
        this.terminal.addKeyListener(new KeyListener(){
            @Override
            public void keyTyped(KeyEvent ke){
        
            }
            @Override
            public void keyPressed(KeyEvent ke){
                
                str+=Character.toString(ke.getKeyChar());
                if(ke.getKeyChar()==KeyEvent.VK_ENTER){
                    try{
                        writer.write(str);
                        writer.flush();
                        str="";
                        
                        terminal.append("\n");
                        terminal.setCaretPosition( terminal.getDocument().getLength() );
                        
                    }catch(IOException e){
                        //System.err.println(e.getMessage());
                    }
                }
                
            }
            @Override
            public void keyReleased(KeyEvent ke){
                
            }  
        }
        );  
    }
    @Override
    public void run(){
        try{
            
            int len;
            
            ProcessBuilder builder = new ProcessBuilder("python","-u","Compilador/CodigoIntermedio/TM.py");
            Process p = builder.start();
            
            reader= new BufferedReader(new InputStreamReader(p.getInputStream()));
            writer=new BufferedWriter(new OutputStreamWriter(p.getOutputStream()));
            
            answer=reader.readLine();
            while(answer!=null){
                if("ENTRADA:".equals(answer)){
                    terminal.append(answer+"\n");
                    len=terminal.getDocument().getLength();
                    terminal.setCaretPosition(len);
                    answer=reader.readLine();
                }else{
                    terminal.append(answer+"\n");
                    len=terminal.getDocument().getLength();
                    terminal.setCaretPosition(len);
                    answer=reader.readLine();
                } 
            }
            
            reader.close();
            writer.close();
            
        }catch(IOException e){
            //System.out.println(e.getMessage());
        }
    }
    
    
    
    
}