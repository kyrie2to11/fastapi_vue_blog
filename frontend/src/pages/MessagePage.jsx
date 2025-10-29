import React, { useState } from 'react';
import { Container, Row, Col, Card, ListGroup, Form, Button, Spinner, Alert } from 'react-bootstrap';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { Link } from 'react-router-dom';
import { fetchMessages, createMessage } from '../services/api';

const MessagePage = () => {
  const queryClient = useQueryClient();
  const [formData, setFormData] = useState({ name: '', email: '', content: '' });
  const [formError, setFormError] = useState('');

  // Fetch messages
  const { data: messages = [], isLoading: isLoadingMessages, error: messagesError } = useQuery('messages', fetchMessages);

  // Create message mutation
  const createMessageMutation = useMutation(createMessage, {
    onSuccess: () => {
      queryClient.invalidateQueries('messages');
      setFormData({ name: '', email: '', content: '' });
      setFormError('');
    },
    onError: (error) => {
      setFormError(error.message || 'Failed to send message. Please try again.');
    }
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.name || !formData.email || !formData.content) {
      setFormError('Please fill in all required fields.');
      return;
    }
    createMessageMutation.mutate(formData);
  };

  if (isLoadingMessages) {
    return (
      <Container className="mt-5 d-flex justify-content-center">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading messages...</span>
        </Spinner>
      </Container>
    );
  }

  return (
    <Container fluid>
      <h1 className="mb-5">Message Board</h1>
      
      <Row>
        <Col md={8}>
          <Card>
            <Card.Header>Send a Message</Card.Header>
            <Card.Body>
              {formError && <Alert variant="danger" className="mb-3">{formError}</Alert>}
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="formName">
                  <Form.Label>Your Name</Form.Label>
                  <Form.Control
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    placeholder="Enter your name"
                    required
                  />
                </Form.Group>
                <Form.Group className="mb-3" controlId="formEmail">
                  <Form.Label>Email Address</Form.Label>
                  <Form.Control
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    placeholder="Enter your email"
                    required
                  />
                </Form.Group>
                <Form.Group className="mb-3" controlId="formContent">
                  <Form.Label>Your Message</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={4}
                    name="content"
                    value={formData.content}
                    onChange={handleInputChange}
                    placeholder="Write your message here..."
                    required
                  />
                </Form.Group>
                <Button 
                  variant="primary" 
                  type="submit"
                  disabled={createMessageMutation.isLoading}
                >
                  {createMessageMutation.isLoading ? <Spinner size="sm" className="me-2" /> : null}
                  Send Message
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>

        <Col md={4}>
          <Card className="mt-4">
            <Card.Header>Messages</Card.Header>
            <Card.Body>
              {messagesError ? (
                <Alert variant="danger">Failed to load messages. Please try again later.</Alert>
              ) : messages.length === 0 ? (
                <Alert variant="info">No messages yet. Be the first to send a message!</Alert>
              ) : (
                <ListGroup>
                  {messages.map((message) => (
                    <ListGroup.Item key={message.id} className="mb-3">
                      <h5 className="mb-1">{message.name}</h5>
                      <p className="text-muted small mb-1">{new Date(message.created_at).toLocaleDateString()}</p>
                      <p className="mb-0">{message.content}</p>
                    </ListGroup.Item>
                  ))}
                </ListGroup>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default MessagePage;