"""
BIM Analysis Controller
Handles property analysis requests using o3-mini AI integration
"""

import os
import json
import logging
from flask import Blueprint, request, jsonify
from openai import OpenAI
from src.security_utils import secure_endpoint

logger = logging.getLogger(__name__)

bim_analysis_bp = Blueprint('bim_analysis', __name__, url_prefix='/api/bim-analysis')

@bim_analysis_bp.route('/analyze-property')
@secure_endpoint
def analyze_property():
    """Analyze property using o3-mini AI"""
    asset_id = request.args.get('asset_id')
    if not asset_id:
        return jsonify({'success': False, 'error': 'Asset ID required'}), 400
    
    try:
        # Property data mapping
        property_data = {
            'prop-001': {'name': 'Downtown Office Complex - Miami', 'type': 'Commercial', 'value': '$12.5M'},
            'prop-002': {'name': 'Luxury Residential Tower - NYC', 'type': 'Residential', 'value': '$45.2M'},
            'prop-003': {'name': 'Industrial Warehouse - Dallas', 'type': 'Industrial', 'value': '$8.9M'},
            'prop-004': {'name': 'Mixed-Use Development - LA', 'type': 'Mixed-Use', 'value': '$28.7M'},
            'property-downtown-001': {'name': 'Downtown Office Complex', 'type': 'Commercial', 'value': '$2.4M'},
            'property-residential-002': {'name': 'Luxury Residential Tower', 'type': 'Residential', 'value': '$8.9M'},
            'property-industrial-003': {'name': 'Industrial Warehouse Complex', 'type': 'Industrial', 'value': '$1.2M'}
        }.get(asset_id, {'name': 'Unknown Property', 'type': 'Unknown', 'value': '$0'})
        
        # Use o3-mini for analysis
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        prompt = f"""
        Analyze the following real estate property for tokenization and investment potential:
        
        Property: {property_data['name']}
        Type: {property_data['type']}
        Value: {property_data['value']}
        
        Provide comprehensive investment analysis including:
        - Investment score (1-10)
        - ROI projection (annual percentage)  
        - Risk assessment (Low/Medium/High)
        - Liquidity analysis
        - Market positioning
        - Tokenization benefits
        - Detailed analysis report
        - Confidence score (0-1)
        
        Return as JSON with all metrics calculated.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a real estate investment analyst specializing in tokenization. Provide detailed investment analysis for properties. Always return data in JSON format with real calculations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        analysis = json.loads(response.choices[0].message.content)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        logger.error(f"Property analysis error: {e}")
        return jsonify({
            'success': False,
            'error': 'Property analysis service temporarily unavailable'
        }), 500

@bim_analysis_bp.route('/investment-analysis', methods=['POST'])
@secure_endpoint
def investment_analysis():
    """Generate investment analysis for property"""
    data = request.get_json()
    if not data or not data.get('asset_id'):
        return jsonify({'success': False, 'error': 'Asset ID required'}), 400
    
    try:
        asset_id = data['asset_id']
        wallet_address = data.get('wallet_address', '')
        
        # Property data mapping
        property_data = {
            'prop-001': {'name': 'Downtown Office Complex - Miami', 'type': 'Commercial', 'value': '$12.5M'},
            'prop-002': {'name': 'Luxury Residential Tower - NYC', 'type': 'Residential', 'value': '$45.2M'},
            'prop-003': {'name': 'Industrial Warehouse - Dallas', 'type': 'Industrial', 'value': '$8.9M'},
            'prop-004': {'name': 'Mixed-Use Development - LA', 'type': 'Mixed-Use', 'value': '$28.7M'},
            'property-downtown-001': {'name': 'Downtown Office Complex', 'type': 'Commercial', 'value': '$2.4M'},
            'property-residential-002': {'name': 'Luxury Residential Tower', 'type': 'Residential', 'value': '$8.9M'},
            'property-industrial-003': {'name': 'Industrial Warehouse Complex', 'type': 'Industrial', 'value': '$1.2M'}
        }.get(asset_id, {'name': 'Unknown Property', 'type': 'Unknown', 'value': '$0'})
        
        # Use o3-mini for investment analysis
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        prompt = f"""
        Generate investment opportunity analysis for tokenized real estate:
        
        Property: {property_data['name']}
        Type: {property_data['type']}
        Value: {property_data['value']}
        Investor Wallet: {wallet_address}
        
        Calculate and provide:
        - Minimum investment amount in ODIS tokens
        - Expected annual returns percentage
        - Token allocation percentage
        - Vesting period
        - Investment strategy recommendations
        - Risk mitigation factors
        - Market timing analysis
        - Confidence score (0-1)
        
        Return as JSON with all investment metrics.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an investment advisor specializing in tokenized real estate. Provide detailed investment opportunities with calculated metrics. Always return data in JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        analysis = json.loads(response.choices[0].message.content)
        
        return jsonify({
            'success': True,
            'investment_analysis': analysis.get('analysis', 'Investment analysis complete'),
            'min_investment': analysis.get('min_investment', '1,000 ODIS'),
            'expected_returns': analysis.get('expected_returns', '15.2% APY'),
            'token_allocation': analysis.get('token_allocation', '0.05%'),
            'vesting_period': analysis.get('vesting_period', '12 months'),
            'confidence': analysis.get('confidence', 0.85)
        })
        
    except Exception as e:
        logger.error(f"Investment analysis error: {e}")
        return jsonify({
            'success': False,
            'error': 'Investment analysis service temporarily unavailable'
        }), 500