pragma solidity >=0.8.0;

contract owned {
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    
    function transferOwnership (address newOwner) public onlyOwner {
        owner = newOwner;
    }
}


contract BasicTOken is owned {
    uint public totalSupply;
    string public name;
    string public symbol;
    uint8 public decimals =18;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowence;
    
    event Transfer(address indexed _from, address indexed _to, uint tokens);
    event Approval(address indexed _tokenOwner, address indexed _spender, uint tokens);
    event Burn(address indexed from, uint256 value);
    
    constructor  (string memory tokenName , string memory tokenSymbol , uint initialSupply)  public {
        totalSupply = initialSupply*10**uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        name = tokenName;
        symbol = tokenSymbol;
    }
    
    function _transfer(address _from, address _to, uint256 _value) internal {
        require(_to != address(0));
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value >= balanceOf[_to]);
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }
    
    function transfer (address _to, uint256 _value) public returns (bool success) {
        _transfer(msg.sender, _to, _value);
        return true;
    }
    
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= allowence[_from][msg.sender]);
        allowence[_from][msg.sender] -= _value;
        _transfer(_from, _to, _value);
        return true;
    }
    
    function mintToken (address _target, uint256 _mintedAmount) public onlyOwner
    {
        balanceOf[_target] += _mintedAmount;
        totalSupply += _mintedAmount;
        emit Transfer(address(0), owner, _mintedAmount);
        emit Transfer(owner, _target, _mintedAmount);
    }
    
    function burn(uint256 _value)public onlyOwner returns(bool success){
        require(balanceOf[msg.sender] >= _value);
        balanceOf[msg.sender]-= _value;
        totalSupply -= _value;
        emit Burn(msg.sender,_value);
        return true;
    }
}
