const express = require('express');
const router = express.Router();

// Example controller function
const getUser = async (req, res) => {
  try {
    const userId = req.params.id;
    // mock DB call
    const user = { id: userId, name: "John Doe" };
    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }
    res.status(200).json(user);
  } catch (error) {
    res.status(500).json({ error: "Internal server error" });
  }
};

router.get('/:id', getUser);

module.exports = router;
