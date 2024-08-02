// components/Popup.tsx
import React, {useState} from 'react';
import popupService from '../services/popupService.tsx';
import { useParams } from 'react-router-dom';
import styles from '../styles/popup.module.css';


interface PopupProps {
  onClose: () => void; // Function to close the popup
}

interface RouteParams {
    id: string ;
}

export const Stocks: React.FC<PopupProps> = ({ onClose }) => {
    const [clickedButton, setClickedButton] = useState<string | null>(null);
    const { id } = useParams<RouteParams>();
    const [ticker, setTicker] = useState<string>('');
    const [quantity, setStockQuantity] = useState<string>('');
    const [price, setStockPrice] = useState<string>('');
    const [message, setMessage] = useState<string>('');

    const handleButtonClick = (value: string) => {
        setClickedButton(value);
    };

    const submitOrder = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
            try {
            var output = ''
            if (clickedButton === 'buy'){
                output = await popupService.addStockToPortfolio(id, ticker, quantity, price) as string;
                setMessage(output)
            }      
            if (clickedButton === 'sell'){
                output = await popupService.removeStockFromPortfolio(id, ticker, quantity, price) as string;
                setMessage(output)
            }
        } catch (error) {
            console.log(error);
            setMessage('Invalid credentials');
        }
    };

    return (
        <div className={`${styles.popup}`}>
          <div className={styles.popupContent}>
            <span className={styles.closeBtn} onClick={onClose}>&times;</span>
            <h2>Stocks</h2>
            <div>
                <form onSubmit={submitOrder} className="form-popup">
                    <div>
                        <label htmlFor="ticker">Ticker </label>
                        <input type="text" id="ticker" value={ticker} onChange={(e) => setTicker(e.target.value)} />
                    </div>
                    <div>
                        <label htmlFor="quantity">Quantity </label>
                        <input type="string" id="quantity" value={quantity} onChange={(e) => setStockQuantity(e.target.value)}/>
                    </div>
                    <div>
                        <label htmlFor="price">Price $</label>
                        <input type="string" id="price" value={price} onChange={(e) => setStockPrice(e.target.value)} />
                    </div>
                    <button type="submit" onClick={() => handleButtonClick('buy')}> Buy </button>
                    <button type="submit" onClick={() => handleButtonClick('sell')}> Sell </button>
                </form>
            </div>
            {message && <p>{message}</p>}
            <button onClick={onClose}>Close</button>
          </div>
        </div>
    );
};

export const Cash: React.FC<PopupProps> = ({ onClose }) => {
    const [clickedButton, setClickedButton] = useState<string | null>(null);
    const { id } = useParams<RouteParams>();
    const [name, setName] = useState<string>('');
    const [amount, setAmount] = useState<string>('');
    const [interest, setInterest] = useState<string>('');
    const [message, setMessage] = useState<string>('');

    const handleButtonClick = (value: string) => {
        setClickedButton(value);
    };

    const submitOrder = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            var output = ''
            if (clickedButton === 'buy'){
                output = await popupService.addCashToPortfolio(id, name, amount, interest) as string;
                setMessage(output)
            }      
            if (clickedButton === 'sell'){
                output = await popupService.removeCashFromPortfolio(id, name, amount, interest) as string;
                setMessage(output)
            }
        } catch (error) {
            console.log(error);
            setMessage('Invalid credentials');
        }
    };

    return (
        <div className={`${styles.popup}`}>
            <div className={styles.popupContent}>
                <span className={styles.closeBtn} onClick={onClose}>&times;</span>
                <h2>Cash</h2>
                    <div>
                        <form onSubmit={submitOrder}>
                        <div>
                            <label htmlFor="name">Name</label>
                            <input type="text" id="name" value={name} onChange={(e) => setName(e.target.value)}/>
                        </div>
                        <div>
                            <label htmlFor="amount">Amount $</label>
                            <input type="string" id="amount" value={amount} onChange={(e) => setAmount(e.target.value)}/>
                        </div>
                        <div>
                            <label htmlFor="interest">Interest %</label>
                            <input type="string" id="interest" value={interest} onChange={(e) => setInterest(e.target.value)}/>
                        </div>
                        <div>
                            <button type="submit" onClick={() => handleButtonClick('buy')}> Add </button>
                            <button type="submit" onClick={() => handleButtonClick('sell')}> Remove </button>
                        </div>             
                        </form>
                    </div>
                <div>
                    {message && <p>{message}</p>}
                    <button onClick={onClose}>Close</button>                
                </div>
            </div>
        </div>
    );
};

export const RealEstate: React.FC<PopupProps> = ({ onClose }) => {
    // const [isMortgaged, setIsMortgaged] = React.useState(false);
    // const [interestRate, setInterestRate] = React.useState('');
    // const [loanTerm, setLoanTerm] = React.useState('');
    // const [amountRemaining, setAmountRemaining] = React.useState('');
    const [clickedButton, setClickedButton] = useState<string | null>(null);
    const { id } = useParams<RouteParams>();
    const [name, setName] = useState<string>('');
    const [worth, setWorth] = useState<string>('');
    //const [interest, setInterest] = useState<string>('');
    const [message, setMessage] = useState<string>('');

    const handleButtonClick = (value: string) => {
        setClickedButton(value);
    };

    const submitOrder = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            var output = ''
            if (clickedButton === 'buy'){
                output = await popupService.addRealEstateToPortfolio(id, name, worth) as string;
                setMessage(output)
            }      
            if (clickedButton === 'sell'){
                output = await popupService.removeRealEstateFromPortfolio(id, name, worth) as string;
                setMessage(output)
            }
        } catch (error) {
            console.log(error);
            setMessage('Invalid credentials');
        }
    };

    return (
        <div className={`${styles.popup}`}>
            <div className={styles.popupContent}>
                <span className={styles.closeBtn} onClick={onClose}>&times;</span>
                <h2>Real Estate</h2>
                <div>
                        <form onSubmit={submitOrder}>
                        <div>
                            <label htmlFor="name">Name</label>
                            <input type="text" id="name" value={name} onChange={(e) => setName(e.target.value)}/>
                        </div>
                        <div>
                            <label htmlFor="worth">Estimated Value $</label>
                            <input type="text" id="worth" value={worth} onChange={(e) => setWorth(e.target.value)}/>
                        </div>
                        { // 
                                            //     <div>
                                            //     <label htmlFor="mortgaged">Currently mortgaged? </label>
                                            //     <input type="checkbox" id="mortgaged" onChange={handleMortgageChange} />
                                            // </div>
                                            // {isMortgaged && (
                                            //     <>
                                            //         <div>
                                            //             <label htmlFor="interestRate">Interest Rate </label>
                                            //             <input type="text" id="interestRate" value={interestRate} onChange={(e) => setInterestRate(e.target.value)} />
                                            //         </div>
                                            //         <div>
                                            //             <label htmlFor="loanTerm">Loan Term </label>
                                            //             <input type="text" id="loanTerm" value={loanTerm} onChange={(e) => setLoanTerm(e.target.value)} />
                                            //         </div>       
                                            //         <div>
                                            //             <label htmlFor="amountRemaining">Amount remaining </label>
                                            //             <input type="text" id="amountRemaining" value={amountRemaining} onChange={(e) => setAmountRemaining(e.target.value)} />
                                            //         </div>              
                                            //     </>
                                            // )}
                        }
                        <div>
                            <button type="submit" onClick={() => handleButtonClick('buy')}> Add </button>
                            <button type="submit" onClick={() => handleButtonClick('sell')}> Remove </button>
                        </div>     
                        </form>
                </div>
                {message && <p>{message}</p>}
                <div>
                    <button onClick={onClose}>Close</button>
                </div>
            </div>
        </div>
    );
};

export const Debt: React.FC<PopupProps> = ({ onClose }) => {
    const [clickedButton, setClickedButton] = useState<string | null>(null);
    const { id } = useParams<RouteParams>();
    const [name, setName] = useState<string>('');
    const [amount, setAmount] = useState<string>('');
    const [interest, setInterest] = useState<string>('');
    const [message, setMessage] = useState<string>('');

    const handleButtonClick = (value: string) => {
        setClickedButton(value);
    };

    const submitOrder = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            var output = ''
            if (clickedButton === 'buy'){
                output = await popupService.addDebtToPortfolio(id, name, amount, interest) as string;
                setMessage(output)
            }      
            if (clickedButton === 'sell'){
                output = await popupService.removeDebtFromPortfolio(id, name, amount, interest) as string;
                setMessage(output)
            }
        } catch (error) {
            console.log(error);
            setMessage('Invalid credentials');
        }
    };

    return (
        <div className={`${styles.popup}`}>
            <div className={styles.popupContent}>
                <span className={styles.closeBtn} onClick={onClose}>&times;</span>
                <h2>Debt</h2>
                    <div>
                        <form onSubmit={submitOrder}>
                        <div>
                            <label htmlFor="name">Name</label>
                            <input type="text" id="name" value={name} onChange={(e) => setName(e.target.value)}/>
                        </div>
                        <div>
                            <label htmlFor="amount">Amount $</label>
                            <input type="string" id="amount" value={amount} onChange={(e) => setAmount(e.target.value)}/>
                        </div>
                        <div>
                            <label htmlFor="interest">Interest %</label>
                            <input type="string" id="interest" value={interest} onChange={(e) => setInterest(e.target.value)}/>
                        </div>
                        <div>
                            <button type="submit" onClick={() => handleButtonClick('buy')}> Add </button>
                            <button type="submit" onClick={() => handleButtonClick('sell')}> Remove </button>
                        </div>             
                        </form>
                    </div>
                <div>
                    {message && <p>{message}</p>}
                    <button onClick={onClose}>Close</button>                
                </div>
            </div>
        </div>
    );
};