function calculateDownpayment() {
    const propertyValue = parseFloat(document.getElementById('propertyValue').value);
    const downpaymentPercentage = parseFloat(document.getElementById('downpaymentPercentage').value);
    if (isNaN(propertyValue) || isNaN(downpaymentPercentage)) {
        document.getElementById('downpaymentResult').textContent = "Please enter valid numbers!";
        return;
    }
    const downpayment = (propertyValue * downpaymentPercentage) / 100;
    document.getElementById('downpaymentResult').textContent = 
        `Required Downpayment: $${downpayment.toFixed(2)}`;
}

function calculateEMI() {
    const loanAmount = parseFloat(document.getElementById('loanAmount').value);
    const annualInterestRate = parseFloat(document.getElementById('interestRate').value);
    const loanTermYears = parseInt(document.getElementById('loanTerm').value);

    if (isNaN(loanAmount) || isNaN(annualInterestRate) || isNaN(loanTermYears)) {
        document.getElementById('emiResult').textContent = "Please enter valid numbers!";
        return;
    }

    const monthlyInterestRate = annualInterestRate / 12 / 100;
    const numberOfPayments = loanTermYears * 12;

    const emi = loanAmount * monthlyInterestRate * 
        Math.pow(1 + monthlyInterestRate, numberOfPayments) / 
        (Math.pow(1 + monthlyInterestRate, numberOfPayments) - 1);

    document.getElementById('emiResult').textContent = 
        `Monthly EMI: $${emi.toFixed(2)}`;
}
