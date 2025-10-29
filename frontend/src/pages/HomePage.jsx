import React from 'react';
import { Container, Jumbotron, Row, Col, Card, ListGroup } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import { fetchRecentArticles } from '../services/api';

const HomePage = () => {
  const { data: articles = [], isLoading } = useQuery('recentArticles', fetchRecentArticles);

  return (
    <Container fluid>
      <Jumbotron className="bg-light mb-4">
        <h1>Welcome to My Personal Blog</h1>
        <p>
          Sharing thoughts, tutorials, and daily learnings.
        </p>
      </Jumbotron>

      <Row>
        <Col md={8}>
          <h2 className="mb-4">Latest Articles</h2>
          {isLoading ? (
            <div>Loading articles...</div>
          ) : (
            <ListGroup>
              {articles.map(article => (
                <ListGroup.Item key={article.id} className="mb-3">
                  <h3>
                    <Link to={`/blog/${article.slug}`}>{article.title}</Link>
                  </h3>
                  <p className="text-muted">{new Date(article.created_at).toLocaleDateString()}</p>
                  <p className="text-truncate">{article.summary || article.content.substring(0, 150)}...</p>
                  <Link to={`/blog/${article.slug}`} className="btn btn-primary">Read More</Link>
                </ListGroup.Item>
              ))}
            </ListGroup>
          )}
        </Col>

        <Col md={4}>
          <Card className="mb-4">
            <Card.Header>About Me</Card.Header>
            <Card.Body>
              <p>Passionate developer learning new technologies daily.</p>
              <p>Interested in Python, FastAPI, React, and open-source projects.</p>
            </Card.Body>
          </Card>

          <Card>
            <Card.Header>Featured Tools</Card.Header>
            <Card.Body>
              <ul className="list-group list-group-flush">
                <li className="list-group-item">
                  <Link to="/tools">View all tools</Link>
                </li>
                <li className="list-group-item">
                  <Link to="/tools/python">Python Resources</Link>
                </li>
                <li className="list-group-item">
                  <Link to="/tools/react">React Components</Link>
                </li>
              </ul>
            </Card.Body>
          </Card>
        
          <Card>
            <Card.Header>Kancolle Companion</Card.Header>
            <Card.Body>
              <Kancolle />
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default HomePage;