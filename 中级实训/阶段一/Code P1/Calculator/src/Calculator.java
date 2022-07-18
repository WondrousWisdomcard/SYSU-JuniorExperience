import java.awt.*; 
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.*;

import javax.swing.border.TitledBorder;
public class Calculator extends JFrame {
	
	private static final long serialVersionUID = 1L;

	public String cal_add(double l, double r) {
		return l + r + "";
	}
	
	public String cal_sub(double l, double r) {
		return l - r + "";
	}
	
	public String cal_mul(double l, double r) {
		return l * r + "";
	}
	
	public String cal_dev(double l, double r) {
		if(r != 0) {
			return l / r + "";
		}
		else {
			return "ERR";
		}
	}
	
    
    public Calculator(){ 
        super("Easy Calculator");
        
        TitledBorder border = new TitledBorder(" "); 
       
        final JTextField operand_left = new JTextField("12",JTextField.CENTER);
        final JTextField operand_right = new JTextField("2",JTextField.CENTER);
        operand_left.setHorizontalAlignment(JTextField.CENTER);
        operand_right.setHorizontalAlignment(JTextField.CENTER);
        
        
        final JLabel operator = new JLabel(" ",JLabel.CENTER);
        final JLabel equal = new JLabel(" = ", JLabel.CENTER);
        final JLabel result = new JLabel(" ",JLabel.CENTER);
        operator.setHorizontalAlignment(JTextField.CENTER);
        equal.setHorizontalAlignment(JTextField.CENTER);
        result.setHorizontalAlignment(JTextField.CENTER);        
        operator.setBorder(border);
        equal.setBorder(border);
        result.setBorder(border);
        
        JButton[] buttons = new JButton[5];        
        buttons[0] = new JButton(" + ");
        buttons[1] = new JButton(" - "); 
        buttons[2] = new JButton(" * ");
        buttons[3] = new JButton(" / ");
        buttons[4] = new JButton(" OK "); 
		
        setLayout(new GridLayout(2,5,10,10));
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        buttons[0].addActionListener(new ActionListener() {
			@Override
             public void actionPerformed(ActionEvent e) {
                 operator.setText(" + ");
             }
        });
        buttons[1].addActionListener(new ActionListener() {
			@Override
             public void actionPerformed(ActionEvent e) {
                 operator.setText(" - ");
             }
        });
        buttons[2].addActionListener(new ActionListener() {
			@Override
             public void actionPerformed(ActionEvent e) {
                 operator.setText(" * ");
             }
        });
        buttons[3].addActionListener(new ActionListener() {
			@Override
			 public void actionPerformed(ActionEvent e) {
			     operator.setText(" / ");
			 }
        });
        
        buttons[4].addActionListener(new ActionListener() {
       	 	@Override
            public void actionPerformed(ActionEvent e) {
       		   try{
       			   	double left = Double.parseDouble(operand_left.getText());
       			   	double right = Double.parseDouble(operand_right.getText());
       			   	
	                if (operator.getText().equals(" + ")) {	                	
	                	result.setText(cal_add(left, right));
	                }
	                else if (operator.getText().equals(" - ")){
	                	result.setText(cal_sub(left, right));
	                }
	                else if (operator.getText().equals(" * ")){
	                	result.setText(cal_mul(left, right));
	                }
	                else if (operator.getText().equals(" / ")){
                		result.setText(cal_dev(left, right));	                	
	                }
	                else {
	                	result.setText(" ");
	                }
               } 
       		   catch(Exception err) {
       		 	    result.setText("Err");
       		   }
       	    }
       	 
       });
        
        add(operand_left);
        add(operator);
        add(operand_right);
        add(equal);
        add(result);
        
        for(int i = 0; i < 5; i++) {
        	add(buttons[i]);
        }
        
        pack(); 
        
        setSize(500,200); 
        setLocation(200,200);  
        setVisible(true);    
    }
    

    public static void main(String[] args) {
    	System.out.println("Running Calculator...");    
        new Calculator();         
        return;
    } 
} 
