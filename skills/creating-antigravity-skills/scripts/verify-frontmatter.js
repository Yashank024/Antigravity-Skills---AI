#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const skillDir = process.argv[2];
if (!skillDir) {
  console.error('Usage: node verify-frontmatter.js <path-to-skill-dir>');
  process.exit(1);
}

const skillMdPath = path.join(skillDir, 'SKILL.md');
if (!fs.existsSync(skillMdPath)) {
  console.error(`❌ SKILL.md not found in ${skillDir}`);
  process.exit(1);
}

const content = fs.readFileSync(skillMdPath, 'utf8');
const frontmatterRegex = /^---\n([\s\S]*?)\n---/;
const match = content.match(frontmatterRegex);

if (!match) {
  console.error('❌ YAML frontmatter missing or incorrectly formatted.');
  process.exit(1);
}

const yaml = match[1];
const nameMatch = yaml.match(/name:\s*([^\n]+)/);
const descMatch = yaml.match(/description:\s*([^\n]+)/);

if (!nameMatch) {
  console.error('❌ "name" missing from frontmatter.');
  process.exit(1);
}

if (!descMatch) {
  console.error('❌ "description" missing from frontmatter.');
  process.exit(1);
}

const name = nameMatch[1].trim();
if (name.length > 64) console.warn('⚠️ Name exceeds 64 characters.');
if (!/^[a-z0-9-]+$/.test(name)) console.error('❌ Name must contain only lowercase letters, numbers, and hyphens.');
if (name.includes('claude') || name.includes('anthropic')) console.error('❌ Name cannot contain "claude" or "anthropic".');

const desc = descMatch[1].trim();
if (desc.length > 1024) console.warn('⚠️ Description exceeds 1024 characters.');

console.log('✅ Frontmatter validation complete.');
