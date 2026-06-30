import numpy as np
from scipy.integrate import odeint
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class SIRHarmModel:
    """
    SIR (Susceptible-Infected-Recovered) epidemiological model adapted for AI harm propagation.
    
    Mathematical model:
    dS/dt = -β * S * I / N    (Susceptible → Infected)
    dI/dt = β * S * I / N - γ * I    (Infected → Recovered)
    dR/dt = γ * I    (Recovered/Neutralized)
    
    Where:
    - S = content not yet exposed to harm
    - I = actively harmful/misleading content
    - R = corrected/safe content
    - β (beta) = harm transmission rate (learned from data)
    - γ (gamma) = correction/recovery rate
    - N = total population (S + I + R)
    """
    
    def __init__(self):
        self.beta = 0.5  # Default transmission rate
        self.gamma = 0.1  # Default recovery rate
        self.fitted = False
    
    def _sir_equations(self, y: Tuple[float, float, float], t: float, 
                      beta: float, gamma: float, N: float) -> List[float]:
        """SIR differential equations for harm propagation."""
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return [dSdt, dIdt, dRdt]
    
    def fit(self, train_data: List[Dict[str, float]], 
            initial_conditions: Tuple[float, float, float] = (90.0, 5.0, 5.0),
            time_points: np.ndarray = None) -> None:
        """
        Fit SIR model parameters (beta, gamma) using grid search on training data.
        
        Args:
            train_data: List of dictionaries with 'S', 'I', 'R' values at different times
            initial_conditions: Initial (S, I, R) values
            time_points: Time points for integration
        """
        if time_points is None:
            time_points = np.linspace(0, 10, 100)
        
        # Grid search for optimal beta and gamma
        best_score = float('inf')
        best_beta, best_gamma = self.beta, self.gamma
        
        # Search over reasonable ranges
        beta_range = np.linspace(0.1, 2.0, 20)
        gamma_range = np.linspace(0.01, 0.5, 20)
        
        for beta in beta_range:
            for gamma in gamma_range:
                try:
                    # Solve ODE
                    solution = odeint(self._sir_equations, 
                                    initial_conditions, 
                                    time_points, 
                                    args=(beta, gamma, sum(initial_conditions)))
                    
                    # Calculate error against training data
                    error = 0.0
                    for i, data_point in enumerate(train_data):
                        if i < len(solution):
                            S_pred, I_pred, R_pred = solution[i]
                            error += (S_pred - data_point.get('S', 0))**2
                            error += (I_pred - data_point.get('I', 0))**2
                            error += (R_pred - data_point.get('R', 0))**2
                    
                    if error < best_score:
                        best_score = error
                        best_beta, best_gamma = beta, gamma
                except Exception:
                    continue
        
        self.beta = best_beta
        self.gamma = best_gamma
        self.fitted = True
    
    def predict(self, initial_conditions: Tuple[float, float, float] = (90.0, 5.0, 5.0),
                time_points: np.ndarray = None) -> np.ndarray:
        """
        Predict SIR trajectories given initial conditions.
        
        Args:
            initial_conditions: Initial (S, I, R) values
            time_points: Time points for integration
        
        Returns:
            Array of shape (len(time_points), 3) containing [S, I, R] values
        """
        if time_points is None:
            time_points = np.linspace(0, 10, 100)
        
        if not self.fitted:
            warnings.warn("Model not fitted. Using default parameters.")
        
        N = sum(initial_conditions)
        solution = odeint(self._sir_equations, 
                         initial_conditions, 
                         time_points, 
                         args=(self.beta, self.gamma, N))
        
        return solution
    
    def score_risk(self, initial_conditions: Tuple[float, float, float] = (90.0, 5.0, 5.0),
                   time_points: np.ndarray = None) -> float:
        """
        Calculate risk score based on infection trajectory.
        
        Args:
            initial_conditions: Initial (S, I, R) values
            time_points: Time points for integration
        
        Returns:
            Risk score between 0 and 100
        """
        if time_points is None:
            time_points = np.linspace(0, 10, 100)
        
        solution = self.predict(initial_conditions, time_points)
        
        # Risk is proportional to peak infection level and duration
        I_values = solution[:, 1]  # All I values
        peak_infection = np.max(I_values)
        infection_duration = np.sum(I_values > 0.1) / len(I_values)
        
        # Normalize to 0-100 scale
        risk_score = min(100.0, (peak_infection * 10 + infection_duration * 50))
        
        return risk_score
    
    def get_parameters(self) -> Dict[str, float]:
        """Get current model parameters."""
        return {
            'beta': self.beta,
            'gamma': self.gamma,
            'fitted': self.fitted
        }
    
    def verify_conservation_law(self, initial_conditions: Tuple[float, float, float]) -> bool:
        """
        Verify that S + I + R remains constant (conservation law).
        
        Returns:
            True if conservation law holds within tolerance
        """
        if not self.fitted:
            return False
        
        time_points = np.linspace(0, 10, 100)
        solution = self.predict(initial_conditions, time_points)
        
        total = solution[:, 0] + solution[:, 1] + solution[:, 2]
        initial_total = sum(initial_conditions)
        
        # Check if total remains within 1% of initial total
        return np.allclose(total, initial_total, rtol=0.01)
import numpy as np
from scipy.integrate import odeint
from typing import List, Dict, Any, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class SIRHarmModel:
    """
    SIR (Susceptible-Infected-Recovered) epidemiological model adapted for 
    harm propagation in AI conversations.
    
    dS/dt = -β * S * I / N    (Susceptible → Infected)
    dI/dt = β * S * I / N - γ * I    (Infected → Recovered)
    dR/dt = γ * I    (Recovered/Neutralized)
    
    Where:
    - S = content not yet exposed to harm
    - I = actively harmful/misleading content
    - R = corrected/safe content
    - β (beta) = harm transmission rate
    - γ (gamma) = correction/recovery rate
    - N = total population (prompt complexity + context)
    """
    
    def __init__(self, beta: float = 0.5, gamma: float = 0.1):
        """
        Initialize SIR harm propagation model.
        
        Args:
            beta: Harm transmission rate (default: 0.5)
            gamma: Correction/recovery rate (default: 0.1)
        """
        self.beta = beta
        self.gamma = gamma
        self.fitted = False
        
    def _sir_equations(self, y: List[float], t: float, beta: float, gamma: float, N: float) -> List[float]:
        """
        SIR differential equations for harm propagation.
        
        Args:
            y: [S, I, R] state vector
            t: time point
            beta: transmission rate
            gamma: recovery rate
            N: total population size
        
        Returns:
            Derivatives [dS/dt, dI/dt, dR/dt]
        """
        S, I, R = y
        dS_dt = -beta * S * I / N
        dI_dt = beta * S * I / N - gamma * I
        dR_dt = gamma * I
        return [dS_dt, dI_dt, dR_dt]
    
    def fit(self, training_data: List[Dict[str, Any]], max_iter: int = 100) -> 'SIRHarmModel':
        """
        Fit model parameters (beta, gamma) to training data using grid search.
        
        Args:
            training_data: List of dictionaries with 'harm_level' and 'context_complexity'
            max_iter: Maximum iterations for parameter optimization
        
        Returns:
            Self for method chaining
        """
        # Simple grid search for demonstration
        best_score = -1
        best_params = (self.beta, self.gamma)
        
        # Sample parameter space
        beta_values = np.linspace(0.1, 2.0, 10)
        gamma_values = np.linspace(0.01, 0.5, 10)
        
        for beta in beta_values:
            for gamma in gamma_values:
                # Calculate score based on training data
                score = self._evaluate_parameters(training_data, beta, gamma)
                if score > best_score:
                    best_score = score
                    best_params = (beta, gamma)
        
        self.beta, self.gamma = best_params
        self.fitted = True
        return self
    
    def _evaluate_parameters(self, training_data: List[Dict[str, Any]], beta: float, gamma: float) -> float:
        """
        Evaluate parameter quality on training data.
        
        Args:
            training_data: Training examples
            beta: Transmission rate to test
            gamma: Recovery rate to test
        
        Returns:
            Score (higher is better)
        """
        total_score = 0
        for example in training_data:
            # Simulate SIR dynamics for this example
            N = example.get('context_complexity', 100)
            initial_state = [N * 0.8, N * 0.1, N * 0.1]  # S, I, R
            t = np.linspace(0, 10, 100)
            
            try:
                solution = odeint(self._sir_equations, initial_state, t, args=(beta, gamma, N))
                # Final infection level should correlate with harm_level
                final_I = solution[-1, 1]
                target_harm = example.get('harm_level', 50)
                # Score based on correlation
                score = 1.0 - abs(final_I / N - target_harm / 100.0)
                total_score += score
            except Exception:
                total_score += 0.1  # Default low score for failed integration
        
        return total_score / len(training_data) if training_data else 0.1
    
    def predict(self, prompt: str, context_complexity: int = 100, 
                max_time: float = 10.0) -> Dict[str, Any]:
        """
        Predict harm propagation trajectory for a given prompt.
        
        Args:
            prompt: Input text to analyze
            context_complexity: Complexity of the context (1-200)
            max_time: Maximum simulation time
        
        Returns:
            Dictionary with SIR trajectory and risk assessment
        """
        if not self.fitted:
            raise ValueError("Model must be fitted before prediction")
        
        # Estimate initial conditions based on prompt analysis
        # Simplified: use length and keyword analysis
        base_I = min(len(prompt) / 20.0, 0.3)  # Base infection from prompt length
        
        # Add keywords-based infection boost
        keywords = ['bleach', 'poison', 'dangerous', 'toxic', 'fake', 'scam', 'fraud']
        for kw in keywords:
            if kw.lower() in prompt.lower():
                base_I += 0.2
        
        base_I = min(base_I, 0.9)
        
        S0 = 1.0 - base_I
        I0 = base_I
        R0 = 0.0
        N = float(context_complexity)
        
        initial_state = [S0 * N, I0 * N, R0 * N]
        t = np.linspace(0, max_time, 100)
        
        try:
            solution = odeint(self._sir_equations, initial_state, t, args=(self.beta, self.gamma, N))
            
            # Extract key metrics
            peak_infection = np.max(solution[:, 1])
            final_infection = solution[-1, 1]
            recovery_rate = solution[-1, 2] / N
            
            return {
                'trajectory': {
                    'time': t.tolist(),
                    'susceptible': solution[:, 0].tolist(),
                    'infected': solution[:, 1].tolist(),
                    'recovered': solution[:, 2].tolist()
                },
                'peak_infection': float(peak_infection / N),
                'final_infection': float(final_infection / N),
                'recovery_rate': float(recovery_rate),
                'risk_probability': float(final_infection / N)
            }
        except Exception as e:
            # Fallback for numerical instability
            return {
                'trajectory': {'time': [], 'susceptible': [], 'infected': [], 'recovered': []},
                'peak_infection': 0.0,
                'final_infection': 0.0,
                'recovery_rate': 0.0,
                'risk_probability': 0.0
            }
    
    def score_risk(self, prompt: str, context_complexity: int = 100) -> float:
        """
        Score risk on 0-100 scale.
        
        Args:
            prompt: Input text to analyze
            context_complexity: Complexity of the context (1-200)
        
        Returns:
            Risk score (0-100)
        """
        prediction = self.predict(prompt, context_complexity)
        
        # Convert probability to 0-100 scale
        risk_prob = prediction['risk_probability']
        
        # Apply non-linear scaling for better discrimination
        risk_score = min(100.0, max(0.0, risk_prob * 120.0))
        
        return risk_score
    
    def get_parameters(self) -> Dict[str, float]:
        """
        Get current model parameters.
        
        Returns:
            Dictionary with beta and gamma values
        """
        return {'beta': self.beta, 'gamma': self.gamma}

# Convenience function
def create_sir_model(beta: float = 0.5, gamma: float = 0.1) -> SIRHarmModel:
    """
    Create and return a new SIR harm model instance.
    
    Args:
        beta: Harm transmission rate
        gamma: Correction/recovery rate
    
    Returns:
        SIRHarmModel instance
    """
    return SIRHarmModel(beta, gamma)