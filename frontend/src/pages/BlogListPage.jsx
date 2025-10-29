import React from 'react';
import { Container, Row, Col, ListGroup, Spinner, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import { fetchAllArticles } from '../services/api';

const BlogListPage = () => {
  const { data: articles = [], isLoading, error } = useQuery('allArticles', fetchAllArticles);

  if (isLoading) {
    return (
      <Container className="mt-5 d-flex justify-content-center">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="mt-5">
        <Alert variant="danger">
          Failed to load articles. Please try again later.
        </Alert>
      </Container>
    );
  }

  return (
    <Container fluid>
      <h1 className="mb-5">All Articles</h1>
      
      {articles.length === 0 ? (
        <Alert variant="info">
          No articles found. Check back soon for new content!
        </Alert>
      ) : (
        <ListGroup>
          {articles.map(article => (
            <ListGroup.Item key={article.id} className="border-0 mb-4 shadow-sm">
              <div className="d-flex justify-content-between align-items-start">
                <div>
                  <h3 className="mb-2">
                    <Link to={`/blog/${article.slug}`} className="text-decoration-none text-dark">
                      {article.title}
                    </Link>
                  </h3>
                  <p className="text-muted mb-2">
                    By {article.author?.username || 'Unknown'} • {new Date(article.created_at).toLocaleDateString()}
                  </p>
                  <p className="text-truncate">{article.summary || article.content.substring(0, 150)}...</p>
                </div>
                <Link
                  to={`/blog/${article.slug}`}
                  className="btn btn-primary align-self-center"
                >
                  Read More
                </Link>
              </div>
            </ListGroup.Item>
          ))}
        </ListGroup>
      )}
    </Container>
  );
};

export default BlogListPage;