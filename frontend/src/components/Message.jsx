import React from 'react';

function isObject(val) {
  return val && typeof val === 'object' && !Array.isArray(val);
}

function Message({ role, content }) {
  const isUser = role === 'user';
  // Prepare the message body
  let body;
  if (isObject(content)) {
    const { name, description, installation, model_compatibility, image_url, part_number } = content;
    body = (
      <div className="product-info">
        {image_url && (
          <img src={image_url} alt={name} className="product-image" />
        )}
        <h4>{name}</h4>
        {part_number && <p className="part-number">Part #{part_number}</p>}
        <p>{description}</p>
        {model_compatibility && model_compatibility.length > 0 && (
          <p className="compatibility">Compatible models: {model_compatibility.join(', ')}</p>
        )}
        {installation && (
          <details>
            <summary>Installation Instructions</summary>
            <p>{installation}</p>
          </details>
        )}
      </div>
    );
  } else {
    body = <p>{content}</p>;
  }

  return (
    <div className={`message ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-bubble">{body}</div>
    </div>
  );
}

export default Message;