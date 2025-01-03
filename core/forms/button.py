from django.utils.html import format_html
from django.utils.safestring import mark_safe
from typing import Optional, Dict, Any

class Button:
    """
    A flexible Button class for Django that can render different HTML tags (a, button, input).
    Always includes 'btn' class and appends additional classes.
    
    Attributes:
        text (str): The text to display on the button
        tag (str): HTML tag to use ('a', 'button', 'input')
        url (str, optional): The URL for link tags
        classes (str): Additional CSS classes to append after 'btn'
        attrs (dict): Additional HTML attributes
        is_disabled (bool): Whether the button should be disabled
    """
    
    VALID_TAGS = ['a', 'button', 'input']
    DEFAULT_CLASS = 'btn'
    
    def __init__(
        self,
        text: str,
        tag: str = 'button',
        url: Optional[str] = None,
        classes: str = '',
        attrs: Optional[Dict[str, Any]] = None,
        is_disabled: bool = False,
        *args,
        **kwargs
    ):
        self.text = text
        self.tag = tag.lower()
        self.url = url
        self.classes = classes
        self.attrs = attrs or {}
        self.is_disabled = is_disabled
        
        # Validate tag
        if self.tag not in self.VALID_TAGS:
            raise ValueError(f"tag must be one of {', '.join(self.VALID_TAGS)}")
        
        # Validate URL for anchor tags
        if self.tag == 'a' and not self.url:
            raise ValueError("URL is required for anchor tags")
    
    def get_classes(self) -> str:
        """Combine default and additional classes."""
        all_classes = [self.DEFAULT_CLASS]
        
        # Add additional classes from self.classes
        if self.classes:
            all_classes.extend(self.classes.split())
            
        # Add additional classes from attrs if they exist
        if 'class' in self.attrs:
            attr_classes = self.attrs.pop('class').split()
            all_classes.extend(attr_classes)
            
        return ' '.join(all_classes)
    
    def get_attrs_string(self) -> str:
        """Convert attributes dictionary to HTML attribute string."""
        attrs = self.attrs.copy()
        
        # Set combined classes
        attrs['class'] = self.get_classes()
            
        # Handle disabled state
        if self.is_disabled:
            if self.tag == 'a':
                attrs['tabindex'] = '-1'
                attrs['aria-disabled'] = 'true'
            else:
                attrs['disabled'] = 'disabled'
        
        # Add URL for anchor tags
        if self.tag == 'a':
            attrs['href'] = self.url
            attrs['role'] = 'button'
        
        # Handle input type
        if self.tag == 'input':
            attrs['type'] = attrs.get('type', 'submit')
            attrs['value'] = self.text
            
        # Convert attributes to string
        return ' '.join([f'{key}="{value}"' for key, value in attrs.items()])
    
    def render(self) -> str:
        """Render the button as HTML."""
        attrs_string = self.get_attrs_string()
        
        if self.tag == 'input':
            html = f'<input {attrs_string} />'
        elif self.tag == 'a':
            html = f'<a {attrs_string}>{self.text}</a>'
        else:  # button
            html = f'<button {attrs_string}>{self.text}</button>'
            
        return mark_safe(html)
    
    def __str__(self) -> str:
        return self.render()