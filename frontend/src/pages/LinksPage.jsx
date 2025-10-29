import React from 'react';
import { Container, Row, Col, Card, Spinner, Alert } from 'react-bootstrap';
import { useQuery } from 'react-query';
import { fetchLinks } from '../services/api';

const LinksPage = () => {
  const { data: links = [], isLoading, error } = useQuery('links', fetchLinks);

  if (isLoading) {
    return (
      <Container className="mt-5 d-flex justify-content-center">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading links...</span>
        </Spinner>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="mt-5">
        <Alert variant="danger">
          Failed to load links. Please try again later.
        </Alert>
      </Container>
    );
  }

  return (
    <Container fluid>
      <h1 className="mb-5">My Links</h1>
      
      {links.length === 0 ? (
        <Alert variant="info">
          No links available yet. Check back later for updates!
        </Alert>
      ) : (
        <Row>
          {links.map(link => (
            <Col md={4} key={link.id} className="mb-4">
              <Card>
                {link.avatar && (
                  <Card.Img 
                    variant="top" 
                    src={link.avatar} 
                    alt={link.name} 
                    className="link-avatar"
                  />
                )}
                <Card.Header>
                  <a 
                    href={link.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-decoration-none"
                  >
                    {link.name}
                  </a>
                </Card.Header>
                <Card.Body>
                  {link.description && (
                    <p className="card-text">{link.description}</p>
                  )}
                  <Card.Text className="text-muted">
                    Category: {link.category || 'Uncategorized'}
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      )}
    </Container>
  );
};

export default LinksPage;